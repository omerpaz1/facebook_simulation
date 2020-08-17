import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import Post,Status,Friends,Friend_req,Round,Ready,WorkersInfo,Log,Score
from users.models import AllLogin,Users_free
from django.contrib.auth.models import User
import threading 
from facebook.views import posts_user_liked
import facebook.algoritem as algo
from properties import adminUser,agent_id,_benefit,_burden,_privacy_loss
import random
import time


def UpDateScore(user_id,CurrentPostsOnRound):
    for p in CurrentPostsOnRound:
            post = Post.objects.filter(id=p).first()
            if post.username_id != user_id:
                _UpdateScorePosts(post.username_id)

def _UpdateScorePosts(userID_ToUpdate):
    user_score = Score.objects.filter(id_user=userID_ToUpdate).first()
    user_score.benefit = user_score.benefit+_benefit

    print(user_score.benefit)
    # user_score.save()

if __name__ == '__main__':
    Posts = [933, 936, 938, 940, 942,937,941]
    UpDateScore(2,Posts)