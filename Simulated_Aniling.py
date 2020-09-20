import os
import django
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.views import addfriend,inEndScreen,confirm_friends,like_post_Agent,home_Agent,log,create_post_Agent,ready,Round
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
import math
from properties import total_rounds
from properties import Users_num
from properties import agent_id
from properties import temp,AF_COST,OF_COST,UL_COST,SL_COST
from timeit import default_timer as timer


# Users_num = 3

# site path 
site_path = 'http://34.89.133.90/'

# DEBUG mode for the prints
DEBUG = True

# Agent info.
userid = agent_id
agent = User.objects.filter(id=userid).first()
PostsIUsed = {}

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
    Optional_SAFE_LikePostsList,Optional_UN_SAFE_LikePostsList = algo.getOptionalLikePosts(userid,current_posts)
    if Optional_SAFE_LikePostsList: # if the there is posts optional to like.
        operations.update({'SL' : Optional_SAFE_LikePostsList})
    if Optional_UN_SAFE_LikePostsList:
        operations.update({'UL' : Optional_UN_SAFE_LikePostsList})

    # 4 -> P
    operations.update({'P' : algo.getAllStatus()})

    # 5 -> N
    operations.update({'N' : 'None'})
    return operations




'''
this function will get all the possible operators that the agent can do in the round.
first, MakeMove will call the function 'PickMove' from the legal moves in the Possible_Operators list.
after he pick a move he send to a function that call 'UnifromPickFromOption'.
this function will pick Unifromly from the specific operation that chooes in uniformly 
After that he will will send to A function that call 'ActionOperation' that send the Request.
return - > Void
'''
def GoToSuccessor(move):
    current_path = site_path
    if move == "OF":
        AgentRequest = MyRequest(method='GET',path=site_path+'home')
        userIdToAdd = getFriendToAdd(Possible_Operators[move])
        userObj = User.objects.filter(id=userIdToAdd).first()
        addfriend(AgentRequest,userObj)
        return "OF", userIdToAdd

    elif move == "AF":
        AgentRequest = MyRequest(method='GET',path=site_path+'home')
        userToConfirm = getFriendToConfirm(Possible_Operators[move])
        userObj = User.objects.filter(id=userToConfirm).first()
        confirm_friends(AgentRequest,userObj)
        return "AF", userToConfirm

    elif move == "SL":
        PostToLike = getPostToLike(Possible_Operators[move])
        AgentRequest = MyRequest(method='POST',path=site_path+'home',params={'post_id': PostToLike})
        like_post_Agent(AgentRequest,"SL")
        return "SL", PostToLike

    elif move == "UL":
        PostToLike = getPostToLike(Possible_Operators[move])
        AgentRequest = MyRequest(method='POST',path=site_path+'home',params={'post_id': PostToLike})
        like_post_Agent(AgentRequest,"UL")
        return "UL", PostToLike

    elif move == "N":
        log(agent.id,"N")
        return "N", "None"

def GoToSuccessorPost(statusID):
        StatusToPost = getStatusToPost(statusID)
        AgentRequest = MyRequest(method='POST',path=current_path+'home' ,params={'user_option_on_feed': StatusToPost})
        home_Agent(AgentRequest)
        return "P", StatusToPost

def getValuePerMove(move):
    if move == "OF":
        return OF_COST
    elif move == "AF":
        return AF_COST
    elif move == "SL":
        return SL_COST
    elif move == "UL":
        return UL_COST
    elif move == "P":
        key = max(PostsIUsed,key=PostsIUsed.get)
        value = PostsIUsed.get(key)
        return key,value
    elif move == "N":
        return 0 



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
def getStatusToPost(statusID):
    status = Status.objects.filter(id=statusID).first().status
    PostsIUsed.pop(statusID)
    return status

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

def acceptor(deltaH,temp):
    return math.exp(deltaH/temp)


# -----------------------------------------Start Simulation -----------------------------------

# # Log in into the Web Page
if(DEBUG):
    print("Try to login to site")

try:
    login_logger(AgentRequest,AgentRequest,AgentRequest.user)
except:
    print('problem with log in')

if(DEBUG):
    print("Login successful to site")


#  waiting to start simulation
if(DEBUG):
    print("Waiting in the Wait page")
users_login = AllLogin.objects.all()
while(len(users_login) < Users_num):
    users_login = AllLogin.objects.all()
    time.sleep(2)

if(DEBUG):
    print("move from the waiting room to Create Post Page")

start = timer()


''' 
in the Create Post page.
'''

if(DEBUG):
    print("Create Post in Create post page")

# ini the status to list
status = Status.objects.all()
for i in status:
    PostsIUsed.update({i.id : i.sumWithOutBenefit})


# Create The First Round!
algo.Post_on_feed(agent.id)
time.sleep(2)
current_path = site_path+'create_post'

key = max(PostsIUsed,key=PostsIUsed.get)
StatusToPost = getStatusToPost(key)
AgentRequest = MyRequest(method='POST',path=current_path ,params={'user_option': StatusToPost})
create_post_Agent(AgentRequest)


if(DEBUG):
    print("Join to the ready room for the first time.")

''' 
Send For the First time the Agent to the Ready Room
'''
current_path = site_path+'ready'
AgentRequest = MyRequest(method='GET',path=current_path)


# First_Possible_Operators = Get_Possible_Operators(userid,current_posts)
users_ready = set(Ready.objects.values_list('user_id', flat=True))
num_round = 1
h = 0.0
while(num_round != total_rounds):
    while(len(users_ready) != Users_num):        
        users_ready = set(Ready.objects.values_list('user_id', flat=True))
        if agent_id not in users_ready and len(users_ready) != Users_num:
            print("Join to Ready")
            Ready.objects.create(user=AgentRequest.user) #create new Ready User
    print("Out of ready, Make Move!")
    timeRound = timer()
    current_posts = algo.Post_on_feed(agent.id)
    time.sleep(2)
    Ready.objects.all().delete()    
    readyList = []

    '''
    Do Here Algoritem and And Send a Request to the operation.
    '''
    Possible_Operators = Get_Possible_Operators(userid,current_posts)

    keys = list(Possible_Operators.keys())
    random.shuffle(keys)
    print("keys = ",keys)
    for move in keys:
        print("move = ",move)
        if move == "P":
            statusID,val = getValuePerMove(move) # return the value + the current value state
        else:
            val = getValuePerMove(move) # return the value + the current value state

        h_new = h + val
        print(f"h = {h} , val = {val} , h_new = {h_new}")
        deltaH = round(h_new - h,2)
        print(f"deltaH = {deltaH}")
        i = total_rounds - num_round
        ran = round(random.random(),2)
        print("round(random.random(),2) < acceptor(deltaH,i) = ",ran,acceptor(deltaH,(i/total_rounds)))
        if h_new - h > 0 or (ran < acceptor(deltaH,(i/total_rounds))): 
            if move == "P":
                oper,success = GoToSuccessorPost(statusID)
            else:
                oper,success = GoToSuccessor(move)
            h = h_new
            break


    print("Possible_Operators For The Current Round:\n")
    print(Possible_Operators)
    print('\n')
    
    print("he did: ", oper,success)
    users_ready = set(Ready.objects.values_list('user_id', flat=True))
    num_round+=1

    startRound = timer()
    print(f"num round = {num_round}")
    while(len(users_ready) < Users_num-1):
        users_ready = set(Ready.objects.values_list('user_id', flat=True))
    endRound = timer()
    print(f"Round Number {num_round}, took: {(endRound-startRound-6)/60} Minutes")

    users_ready = set(Ready.objects.values_list('user_id', flat=True))
    print('----------------  # End Round----------------\n')

Ready.objects.create(user=AgentRequest.user) #create new Ready User
users_ready = set(Ready.objects.values_list('user_id', flat=True))

while(len(users_ready) != Users_num):        
        users_ready = set(Ready.objects.values_list('user_id', flat=True))

time.sleep(5)
Ready.objects.all().delete()    
readyList = []

end = timer()
algo.UpdateScoreStatic(userid)
print("Simulrator Finished")
print("Total time simulation = ",(end-start)/60, "Minutes")