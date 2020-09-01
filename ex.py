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
    # User = User.objects.filter(id=1).first()
    # # AllLogin.objects.filter(user=User).delete()

    #                 worker_id = request.POST.get('Worker_ID',False)
    #             UserId = Users_free.objects.filter(worker_id=worker_id).first().user_id
    #             UserF = User.objects.filter(id=UserId).first()
    #             login(request,UserF)