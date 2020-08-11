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
import properties

class Agent:
    
    

    def __init__(self,path, user,rounds):
        super().__init__()
        self.path = path
        self.user = user
        self.rounds = rounds

    def CreateRequest(self,method,params):
        req = WSGIRequest({
                'REQUEST_METHOD': method,
                'PATH_INFO': self.path,
                'wsgi.input': StringIO()})

        req.user = self.user
        req.content_params = params
        return req
    
    

if __name__ == "__main__":
    userid = 2
    omerpazUser = User.objects.filter(id=userid).first()
    site_path = properties.site_path
    a1 = Agent(path=site_path, user=omerpazUser,rounds=10)
    AgentRequest = a1.CreateRequest(method='GET',params={"omer": "pro"})
    print(AgentRequest.content_params)
    