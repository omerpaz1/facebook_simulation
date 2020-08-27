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
from properties import adminUser,agent_id,_benefit,_burden,_privacy_loss
import random
import time

def sortbyTime(e):
    return e.date_posted

if __name__ == '__main__':
    #final score = -1.33227e-15
    # priavcy loss = 7.4
    # benefits = 2.1
    # burden = 5.3
    ans = 0
    userScore = Score.objects.filter(id_user=3).first()
    userScore.privacy_loss = 7.4
    userScore.benefit = 2.1
    userScore.burden = 5.3
    userScore.save()
    algo.UpdateScoreStatic(3)
    