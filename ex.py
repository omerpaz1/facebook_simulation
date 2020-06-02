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

'''
this function will return list of the name of the relevant operations.
param: AR - AgentRequest
the operations: 
1. AF (Add Friend)
2. CF (Confirm Friend)
3. LP (Like Post)
4. CP (Create Post)
5. P (Pass)
'''
def Get_Possible_Operators(userid):
    pass



def getStatusToPost():
    print("here")
    all_statuss = list(Status.objects.values_list('status', flat=True)) 
    random_num = random.randint(0,len(all_statuss)-1) # unifom random in all the status.
    return all_statuss[random_num]

def getPostToLike(OptionalPostsToLike):
    random_num = random.randint(0,len(OptionalPostsToLike)-1) # unifom random in all the status.
    return OptionalPostsToLike[random_num]


if __name__ == '__main__':
    # operations = {}
    # # new_round = Round(round_number=len(Round.objects.all())+1,posts_id=[],likes_id=[])

    # # 1 -> AF
    # PeopleMayKnow = algo.getPeopleMayKnow(1)
    # if PeopleMayKnow: # if there is users not in your friends
    #     operations.update({'AF' : PeopleMayKnow})

    # # 2 -> CF
    # FriendRequests = algo.getFriendsRequest(1)
    # if FriendRequests: # if there is users in your friends requests
    #     operations.update({'CF' : FriendRequests})

    # # 3 -> LP
    # PostsOnFeed = algo.getOptionalLikePosts(1,[])
    # if PostsOnFeed: # if the there is posts optional to like.
    #     operations.update({'LP' : PostsOnFeed})

    # # 4 -> CP
    # operations.update({'CP' : algo.getAllStatus()})

    # # 5 -> P
    # operations.update({'P' : 'Pass'})


    # PostsOnFeed = [245,133]
    # move = "LP"

    # if move == "AF":
    #     print(f'Pick = {move}')
    #     print(operations[move])
    # elif move == "CF":
    #     print(getStatusToPost())
    # elif move == "LP":
    #     print(getPostToLike(PostsOnFeed))
    # elif move == "CP":
    #     print(operations[move])
    # elif move == "P":
    #     print(f'Pick = {move}')
    #     print(operations[move]) 
    readyList = list(Ready.objects.values_list('user_id', flat=True))
    print(readyList)