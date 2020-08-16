import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import Post,Status,Friends,Friend_req,Round,Ready,WorkersInfo,Log
from users.models import AllLogin,Users_free
from django.contrib.auth.models import User
import threading 
from facebook.views import posts_user_liked
import facebook.algoritem as algo
from properties import adminUser,agent_id
import random
import time



if __name__ == '__main__':
    print(type(adminUser))
    allusers = User.objects.all()
    for i in allusers:
        print(type(i.id))

    # Optional_SAFE_LikePostsList = []
    # Optional_UN_SAFE_LikePostsList = [] 
    # for key,value in no_likes_LC.items(): # about post with no like. same probability.]
    #     if key in currentPostsOnFeed:
    #         if value == -1:
    #             post = Post.objects.filter(id=key).first()
    #             status =  Status.objects.filter(id=post.status_id).first()
    #             if status.has_link:
    #                 Optional_UN_SAFE_LikePostsList.append(key)
    #             else:
    #                 Optional_SAFE_LikePostsList.append(key)