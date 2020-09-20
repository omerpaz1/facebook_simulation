import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import Post,Status,Friends,Friend_req,Round,Ready,WorkersInfo,Log,Score,benefitRounds2
from users.models import AllLogin,Users_free
from django.contrib.auth.models import User
import threading 
import math
from facebook.views import posts_user_liked
import facebook.algoritem as algo
from properties import adminUser
import random
from timeit import default_timer as timer
import time

if __name__ == '__main__':
    # AllLogin.objects.all().delete()
    start = timer()
    for i in range(5):
        startRound = timer()
        time.sleep(5)
        endRound = timer()
        print("round took: ",endRound-startRound)
    end = timer()

    print("total = ",end-start)
