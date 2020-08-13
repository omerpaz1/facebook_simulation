import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import Post,Status,Friends,Friend_req,Round,Ready,WorkersInfo,Log
from users.models import AllLogin,Users_free
from django.contrib.auth.models import User
import threading 
from facebook.views import posts_user_liked
import random
import time



if __name__ == '__main__':
    pick = Status.objects.all()
    aa =  Status.objects.filter(id=5).first()
    print(aa.has_link)