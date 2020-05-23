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
try:
    login_logger(AgentRequest,AgentRequest,AgentRequest.user)
except:
    print('problem with log in')

# # waiting to start simulation
# users_login = AllLogin.objects.all()
# while(len(users_login) < Users_num):
#     users_login = AllLogin.objects.all()
#     time.sleep(2)

''' 
in the Create Post page.
'''
time.sleep(2)
current_path = 'http://34.89.188.107/create_post'
AgentRequest = MyRequest(method='POST',path=current_path ,params={'user_option': create_post_status})
create_post(AgentRequest)

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

    Possible_Operators = Get_Possible_Operators(AgentRequest)
    random_num = random.uniform(0,1)
    random_num = float('{0:.1f}'.format(random.uniform(0,1)))


    round+=1



def Get_Possible_Operators(request):
    operations = {}
    pass


