import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import Post,Status,Friends,Friend_req,Round,Ready,WorkersInfo
from users.models import AllLogin
from django.contrib.auth.models import User
import threading 
from facebook.views import posts_user_liked
import random
import time




if __name__ == '__main__':
    a = len(Round.objects.all())+1
    print(a)
    WorkersInfo.objects.all().delete()    
