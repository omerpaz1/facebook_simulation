import os
import django
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.views import *
import time
from django.contrib.auth.models import User
from facebook.models import Post,Status,Friends,Friend_req,Ready
from users.views import *
import requests
from django.contrib.auth.models import AnonymousUser
from django.core.handlers.wsgi import WSGIRequest
from io import StringIO ## for Python 3
from django.urls import resolve
import random
import facebook.algoritem as algo
from timeit import default_timer as timer

from properties import total_rounds
from properties import Users_num
from properties import agent_id

# site path 
site_path = 'http://34.89.133.90/'

# DEBUG mode for the prints
DEBUG = True

# Agent info.
userid = agent_id
agent = User.objects.filter(id=userid).first()


def MyRequest(method='GET',path=site_path, user=agent, params={}):
  """ Construct a fake request(WSGIRequest) object"""
  req = WSGIRequest({
          'REQUEST_METHOD': method,
          'PATH_INFO': path,
          'wsgi.input': StringIO()})

  req.user = user

  req.content_params = params
  return req
AgentRequest = MyRequest(method='POST',path=site_path+'login')

'''
this function will return list of the name of the relevant operations.
param: AR - AgentRequest
the operations: 
1. OF (Offer Friendship)
2. AF (Accept Friendship)
3. SL (Safe like link)
4. UL (UnSafe like link)
4. P (Post)
5. N (None)
'''
def Get_Possible_Operators(userid,current_posts):
    operations = {}

    # 1 -> OF
    PeopleMayKnow = algo.getPeopleMayKnow(userid)
    if PeopleMayKnow: # if there is users not in your friends
        operations.update({'OF' : PeopleMayKnow})

    # 2 -> AF
    FriendRequests = algo.getFriendsRequest(userid)
    if FriendRequests: # if there is users in your friends requests
        operations.update({'AF' : FriendRequests})

    # 3 -> SL
    Optional_SAFE_LikePostsList,Optional_UN_SAFE_LikePostsList = getOptinalLikesPostsAll(userid,current_posts)
    if Optional_SAFE_LikePostsList: # if the there is posts optional to like.
        operations.update({'SL' : Optional_SAFE_LikePostsList})
    if Optional_UN_SAFE_LikePostsList:
        operations.update({'UL' : Optional_UN_SAFE_LikePostsList})

    # 4 -> P
    operations.update({'P' : "Posts"})

    # 5 -> N
    operations.update({'N' : 'None'})
    return operations



def getOptinalLikesPostsAll(userid,current_posts):
    currentPostsOnFeed = algo.getIdPosts(current_posts)
    Optional_SAFE_LikePostsList = []
    Optional_UN_SAFE_LikePostsList = []
    for p in currentPostsOnFeed: # about post with no like. same probability.]
        post = Post.objects.filter(id=p).first()
        if post.username_id != userid:
                post_i_liked = post.likes.filter(id=userid).values_list('likes', flat=True).first()
                if post_i_liked != None:
                    continue
                status =  Status.objects.filter(id=post.status_id).first()
                if status.has_link:
                    Optional_UN_SAFE_LikePostsList.append(p)
                else:
                    Optional_SAFE_LikePostsList.append(p)
    return Optional_SAFE_LikePostsList,Optional_UN_SAFE_LikePostsList



'''
this function will get all the possible operators that the agent can do in the round.
first, MakeMove will call the function 'PickMove' from the legal moves in the Possible_Operators list.
after he pick a move he send to a function that call 'UnifromPickFromOption'.
this function will pick Unifromly from the specific operation that chooes in uniformly 
After that he will will send to A function that call 'ActionOperation' that send the Request.
return - > Void
'''
def MakeMove(userid,move,Possible_Operators):
    current_path = site_path
    if move == "OF":
        userObj = User.objects.filter(id=userid).first()
        AgentRequest = MyRequest(method='GET',user= userObj, path=site_path+'home')
        userIdToAdd = getFriendToAdd(Possible_Operators[move])
        userObj = User.objects.filter(id=userIdToAdd).first()
        addfriend(AgentRequest,userObj)
        print("OF", userIdToAdd)
        return "OF", userIdToAdd

    elif move == "AF":
        userObj = User.objects.filter(id=userid).first()
        AgentRequest = MyRequest(method='GET',user= userObj,path=site_path+'home')
        userToConfirm = getFriendToConfirm(Possible_Operators[move])
        userObj = User.objects.filter(id=userToConfirm).first()
        confirm_friends(AgentRequest,userObj)
        print("AF", userToConfirm)
        return "AF", userToConfirm

    elif move == "SL":
        userObj = User.objects.filter(id=userid).first()
        PostToLike = getPostToLike(Possible_Operators[move])
        AgentRequest = MyRequest(method='POST',path=site_path+'home',user= userObj,params={'post_id': PostToLike})
        like_post_Agent(AgentRequest,"SL")
        print("SL", PostToLike)
        return "SL", PostToLike

    elif move == "UL":
        userObj = User.objects.filter(id=userid).first()
        PostToLike = getPostToLike(Possible_Operators[move])
        AgentRequest = MyRequest(method='POST',path=site_path+'home',user= userObj,params={'post_id': PostToLike})
        like_post_Agent(AgentRequest,"UL")
        print("UL", PostToLike)
        return "UL", PostToLike

    elif move == "P":
        userObj = User.objects.filter(id=userid).first()
        StatusToPost,StatusToPostID = getStatusToPost()
        AgentRequest = MyRequest(method='POST',path=current_path+'home' ,user= userObj,params={'user_option_on_feed': StatusToPost})
        home_Agent(AgentRequest)
        print("P", StatusToPost, StatusToPostID)
        return "P", StatusToPostID

    elif move == "N":
        log(agent.id,"N")
        return "N", "None"



'''
this function will pick from the possible opeation one type of operation.. like (AF , N , P, LS , CF)
'SizeOfOp' will be the size of the possible operations for the round.
'''
def PickMove(Possible_Operators):
    SizeOfOp = len(Possible_Operators)
    random_num = random.randint(0,len(Possible_Operators)-1)
    j = 0
    for move in Possible_Operators:
        if j is random_num:
            MovePicked = move
        j+=1
    return MovePicked

'''
this function will return status from all the status in unfomly way.
'''
def getStatusToPost():
    all_statuss = list(Status.objects.values_list('status', flat=True)) 
    random_num = random.randint(0,len(all_statuss)-1) # unifom random in all the status.
    statusPick = all_statuss[random_num]
    return statusPick,Status.objects.filter(status=statusPick).first().id

def getStatusToPostID():
    all_statuss = list(Status.objects.values_list('status', flat=True)) 
    random_num = random.randint(0,len(all_statuss)-1) # unifom random in all the status.
    statusPick = all_statuss[random_num]
    return Status.objects.filter(status=statusPick).first().id

'''
this function will return from the optional 'people you may know' list one user id in unifomly way
'''
def getFriendToAdd(PeopleMayKnowList):
    random_num = random.randint(0,len(PeopleMayKnowList)-1) # unifom random in all the status.
    return PeopleMayKnowList[random_num]

'''
this function will return post that optinal to like in unimofly way.
'''
def getPostToLike(OptionalPostsToLike):
    random_num = random.randint(0,len(OptionalPostsToLike)-1) # unifom random in all the status.
    return OptionalPostsToLike[random_num]

'''
this function will return post that optinal to friend to confirm in unimofly way.
'''
def getFriendToConfirm(FriendRequests):
    random_num = random.randint(0,len(FriendRequests)-1) # unifom random in all the status.
    return FriendRequests[random_num]