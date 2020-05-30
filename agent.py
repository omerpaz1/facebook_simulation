import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
import time
from django.contrib.auth.models import User
from facebook.models import Post,Status,Friends,Friend_req,Ready
from users.views import *
from facebook.views import *
import requests
from django.contrib.auth.models import AnonymousUser
from django.core.handlers.wsgi import WSGIRequest
from io import StringIO ## for Python 3
from django.urls import resolve
import random
import facebook.algoritem as algo


# DEBUG mode for the prints
DEBUG = False

# Agent info.
userid = 1
agent = User.objects.filter(id=userid).first()

#Total rounds untill agnet stop action
total_rounds = 50

# wating and ready values.
Users_num = 3

# create first post values
create_post_status = 'Hello World'
creat_post_path = 'http://34.89.188.107/create_post'

#get the users ready
users_ready = set(Ready.objects.values_list('user_id', flat=True))


def MyRequest(method='GET',path='http://34.89.188.107/', user=agent, params={}):
  """ Construct a fake request(WSGIRequest) object"""
  req = WSGIRequest({
          'REQUEST_METHOD': method,
          'PATH_INFO': path,
          'wsgi.input': StringIO()})

  req.user = user
  req.content_params = params
  return req
AgentRequest = MyRequest(method='POST')


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

time.sleep(2)
current_path = 'http://34.89.188.107/create_post'
AgentRequest = MyRequest(method='POST',path=current_path ,params={'user_option': create_post_status})
create_post(AgentRequest)



if(DEBUG):
    print("Join to the ready room for the first time.")

''' 
Send For the First time the Agent to the Ready Room
'''
current_path = 'http://34.89.188.107/ready'
AgentRequest = MyRequest(method='GET',path=current_path)
ready(AgentRequest)

round = 0
while(round != total_rounds):
    while(agent.id in users_ready):
        time.sleep(3)

    # Possible_Operators is a list with the names of the operator that relevaents.
    Possible_Operators = Get_Possible_Operators(AgentRequest)
    print(Possible_Operators)
    random_num = random.uniform(0,1)
    random_num = float('{0:.1f}'.format(random.uniform(0,1)))


    round+=1


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
def Get_Possible_Operators(AR):
    operations = {}

    # 1 -> AF
    PeopleMayKnow = algo.getPeopleMayKnow(AR.user.id)
    if PeopleMayKnow: # if there is users not in your friends
        operations.update({PeopleMayKnow : 'AF'})

    # 2 -> CF
    FriendRequests = algo.getFriendsRequest(AR.user.id)
    if FriendRequests: # if there is users in your friends requests
        operations.update({FriendRequests : 'CF'})

    # 3 -> LP
    PostsOnFeed = algo.getOptionalLikePosts(AR.user.id)
    if PostsOnFeed: # if the there is posts optional to like.
        operations.update({PostsOnFeed : 'LP'})

    # 4 -> CP
    operations.update({algo.getStatusToPost() : 'CP'})

    # 5 -> P
    operations.update({'Pass' : 'P'})