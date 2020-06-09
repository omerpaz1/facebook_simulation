import os
import django
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.views import addfriend,confirm_friends,like_post_Agent,home_Agent,log,create_post_Agent,ready
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


from properties import total_rounds
from properties import Users_num
from properties import status_id
from properties import agent_id


# site path 
site_path = 'http://34.89.188.107/'

# DEBUG mode for the prints
DEBUG = True

# Agent info.
userid = agent_id
agent = User.objects.filter(id=userid).first()




# create first post values
all_statuss = list(Status.objects.values_list('status', flat=True)) 
create_post_status = all_statuss[status_id]
creat_post_path = site_path+'create_post'


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
1. AF (Add Friend)
2. CF (Confirm Friend)
3. LP (Like Post)
4. CP (Create Post)
5. P (Pass)
'''
def Get_Possible_Operators(userid,current_posts):
    operations = {}

    # 1 -> AF
    PeopleMayKnow = algo.getPeopleMayKnow(userid)
    if PeopleMayKnow: # if there is users not in your friends
        operations.update({'AF' : PeopleMayKnow})

    # 2 -> CF
    FriendRequests = algo.getFriendsRequest(userid)
    if FriendRequests: # if there is users in your friends requests
        operations.update({'CF' : FriendRequests})

    # 3 -> LP
    OptionalPostsToLike = algo.getOptionalLikePosts(userid,current_posts)
    if OptionalPostsToLike: # if the there is posts optional to like.
        operations.update({'LP' : OptionalPostsToLike})

    # 4 -> CP
    operations.update({'CP' : algo.getAllStatus()})

    # 5 -> P
    operations.update({'P' : 'Pass'})
    return operations




'''
this function will get all the possible operators that the agent can do in the round.
first, MakeMove will call the function 'PickMove' from the legal moves in the Possible_Operators list.
after he pick a move he send to a function that call 'UnifromPickFromOption'.
this function will pick Unifromly from the specific operation that chooes in uniformly 
After that he will will send to A function that call 'ActionOperation' that send the Request.
return - > Void

'''
def MakeMove(Possible_Operators):
    move = PickMove(Possible_Operators)
    current_path = site_path
    if move == "AF":
        AgentRequest = MyRequest(method='GET',path=site_path+'home')
        userIdToAdd = getFriendToAdd(Possible_Operators[move])
        userObj = User.objects.filter(id=userIdToAdd).first()
        addfriend(AgentRequest,userObj)
        return "AF", userIdToAdd

    elif move == "CF":
        AgentRequest = MyRequest(method='GET',path=site_path+'home')
        userToConfirm = getFriendToConfirm(Possible_Operators[move])
        userObj = User.objects.filter(id=userToConfirm).first()
        confirm_friends(AgentRequest,userObj)
        return "CF", userToConfirm

    elif move == "LP":
        PostToLike = getPostToLike(Possible_Operators[move])
        AgentRequest = MyRequest(method='POST',path=site_path+'home',params={'post_id': PostToLike})
        like_post_Agent(AgentRequest)
        return "LP", PostToLike

    elif move == "CP":
        StatusToPost = getStatusToPost()
        AgentRequest = MyRequest(method='POST',path=current_path+'home' ,params={'user_option_on_feed': StatusToPost})
        home_Agent(AgentRequest)
        return "CP", StatusToPost

    elif move == "P":
        log(agent.id,"P")
        return "P", "Pass"



'''
this function will pick from the possible opeation one type of operation.. like (AF , P , CP, LP , CF)
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
    return all_statuss[random_num]

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


''' 
in the Create Post page.
'''

if(DEBUG):
    print("Create Post in Create post page")

# Create The First Round!
current_posts = algo.Post_on_feed(agent.id)

time.sleep(2)
current_path = site_path+'create_post'
AgentRequest = MyRequest(method='POST',path=current_path ,params={'user_option': create_post_status})
create_post_Agent(AgentRequest)




if(DEBUG):
    print("Join to the ready room for the first time.")

''' 
Send For the First time the Agent to the Ready Room
'''
current_path = site_path+'ready'
AgentRequest = MyRequest(method='GET',path=current_path)
ready(AgentRequest)


users_ready = set(Ready.objects.values_list('user_id', flat=True))
First_Possible_Operators = Get_Possible_Operators(userid,current_posts)
num_round = 1
while(num_round != total_rounds):
    while(agent.id in users_ready):
        users_ready = set(Ready.objects.values_list('user_id', flat=True))
        ready(AgentRequest)
        time.sleep(2)

    '''
    Do Here Algoritem and And Send a Request to the operation.
    '''
    if First_Possible_Operators is not None:
        Possible_Operators = First_Possible_Operators
        First_Possible_Operators = None
    else:
        Possible_Operators = Get_Possible_Operators(userid,current_posts)
    current_posts = algo.Post_on_feed(agent.id)
    print("Possible_Operators For The Current Round:\n")
    print(Possible_Operators)
    print('\n')
    operand, value = MakeMove(Possible_Operators)
    print(f'MakeMove Pick: Operator = {operand} , value = {value}\n')

    current_path = site_path+'ready'
    AgentRequest = MyRequest(method='GET',path=current_path)
    ready(AgentRequest)
    users_ready = set(Ready.objects.values_list('user_id', flat=True))
    num_round+=1
    print('----------------  # End Round----------------\n')

print("Simulrator Finished")