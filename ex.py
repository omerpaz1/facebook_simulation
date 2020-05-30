import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import Post,Status,Friends,Friend_req,Round,Ready
from users.models import AllLogin
from django.contrib.auth.models import User
import threading 
from facebook.views import posts_user_liked
import random
import time
import facebook.algoritem as algo



if __name__ == '__main__':
    # simulator.simulator()
    # mylist = algo.getOptionalLikePosts(1)
    # print(mylist)
    operations = {}

    # 1 -> AF
    PeopleMayKnow = algo.getPeopleMayKnow(1)
    if PeopleMayKnow: # if there is users not in your friends
        operations.update({'AF' : PeopleMayKnow })

    # 2 -> CF
    FriendRequests = algo.getFriendsRequest(1)
    if FriendRequests: # if there is users in your friends requests
        operations.update({'CF' : FriendRequests})

    # 3 -> LP
    PostsOnFeed = algo.getOptionalLikePosts(1)
    if PostsOnFeed: # if the there is posts optional to like.
        operations.update({'LP' : PostsOnFeed})

    # 4 -> CP
    operations.update({'CP' : algo.getStatusToPost()})

    # 5 -> P
    operations.update({'P' : 'Pass'})


    print(operations)