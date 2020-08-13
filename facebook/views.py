from django.shortcuts import render , redirect
from .models import Post,Status,Friends,Friend_req,Round,WorkersInfo,Log,Ready
from users.models import AllLogin
from django.contrib.auth.models import User
from django.views.generic import ListView,DeleteView,CreateView
from django.contrib.auth.decorators import login_required
import time
import facebook.algoritem as algo
import logging
import sys
from django.http import HttpRequest

# number of Rounds:
from properties import total_rounds
from properties import agent_id

# total users To the Simulation:
from properties import Users_num

Users_num = 3

def ready(request):        
    readyList = set(Ready.objects.values_list('user_id', flat=True))
    if request.user.id not in readyList:
        Ready.objects.create(user=request.user) #create new Ready User
        return render(request,'facebook/ready.html')

    while(len(readyList) != Users_num):
        readyList = set(Ready.objects.values_list('user_id', flat=True))

   
    readyList = []
    return redirect('/home')



def waiting(request):
    users_login = AllLogin.objects.all()
    set_users_login = set()
    for i in users_login:
        set_users_login.add(i.user.id)
    users_login = set_users_login
    while(len(users_login) < Users_num):
        users_login = AllLogin.objects.all()
        for i in users_login:
            set_users_login.add(i.user.id)
        users_login = set_users_login
        context = {
            'active_users' :users_login,
            'allusers': User.objects.all(),
            'left_Users': 5-len(users_login)
        }
        return render(request,'facebook/waiting.html',context)
    time.sleep(1) 
    return redirect('/create_post')
    
@login_required
def end(request):
    if request.method == 'POST':
        worker_id = request.POST.get('Worker_ID',False) 
        free_comments  = request.POST.get('Free_Comments',False) 
        w = WorkersInfo(worker_id=worker_id,free_comments=free_comments)
        w.save()

        return redirect('/logout')
    return render(request,'facebook/end.html')


@login_required
def home(request):
    posts = algo.Post_on_feed(request.user.id)

    user_liked = posts_user_liked(request.user.id)
    people_may_know = helper(request)
    list_friend_req = myreqest(request.user.id)
    

    context = {
        # 'posts' : Post.objects.order_by('-date_posted'),
        'posts' : posts,
        'mystatus' : Status.objects.all(),
        'friends' : Friends.objects.filter(userid_id=request.user.id).first().myfriends,
        'friends_requst' : list(set(Friend_req.objects.filter(userid_id=request.user.id).first().myfriends_req)),
        'people_my_know' : people_may_know,
        'users' : User.objects.all(),
        'posts_user_liked' : user_liked,
        'list_friend_req' : list_friend_req
    }
    if request.method == 'POST':
       user_post_option = request.POST.get('user_option_on_feed',False) 
       user_post_name = request.user
       pick = Status.objects.get(status = user_post_option)
       new_post = Post(username = user_post_name ,status =pick)
       new_post.save()
       log(request.user.id,"CP")
       if len(Round.objects.all()) == total_rounds:
            return redirect('/end')
       return redirect('/ready')
    if len(Round.objects.all()) == total_rounds:
        return redirect('/end')
    return render(request,'facebook/feed.html',context)



@login_required
# function to create post
def create_post(request):
    context = {
        'mystatus' : Status.objects.all(),
        'posts' : Post.objects.all()
    }
    if request.method == 'POST':
       user_post_option = request.POST.get('user_option',False)
       user_post_name = request.user
       pick = Status.objects.get(status = user_post_option)
       new_post = Post(username = user_post_name ,status = pick)
       new_post.save()
       log(request.user.id,"CP")
       return redirect('/ready')

    return render(request,'facebook/post_form.html',context)

    
# function when user click on the "like" btn.

def like_post(request):
    if request.method == 'POST':
        post_like_id = request.POST.get('post_id',False)
        post_like_id = Post.objects.get(id=post_like_id)
        post_like_id.likes.add(request.user)
        log(request.user.id,"LP")
    return redirect('/ready')


'''
request is the user that send the request offering 
user_requsted is the user that we send to him friend request.
'''
def manage_friends(request,operation,pk):
    user_requsted = User.objects.get(pk=pk)
    if operation =='friend_requset':
        addfriend(request,user_requsted)
    if operation == 'friend_confirm':
        confirm_friends(request,user_requsted)
    return redirect('/ready')

# function that help manage the "people you may know"
def helper(request):
    friends = Friends.objects.filter(userid_id=request.user.id).first().myfriends
    friends_requst = list(set(Friend_req.objects.filter(userid_id=request.user.id).first().myfriends_req))
    users = User.objects.all()
    friend_my_know = []
    for c_user in users:
        if c_user.pk not in friends_requst:
            if c_user.pk not in friends:
                if c_user.pk != request.user.id:
                    if c_user.pk != 1:
                        friend_my_know.append(c_user)
    return friend_my_know
# user_requsted = the user that i want to add to my friends.

def addfriend(request ,user_requsted):
    current_user = Friend_req.objects.filter(userid_id=request.user.id).first()
    if user_requsted.pk in current_user.myfriends_req: # if 3 in 5
        confirm_friends(request,user_requsted)
    else:
        user_requsted = Friend_req.objects.filter(userid_id=user_requsted.id).first()
        if current_user.userid_id not in user_requsted.myfriends_req:
            user_requsted.myfriends_req.append(request.user.id)
            user_requsted.save()
    log(request.user.id,"AF")

# comfirm both friend in the tables
def confirm_friends(request,user_requsted):
    current_user_table = Friend_req.objects.filter(userid_id=request.user.id).first()
    current_user_table.myfriends_req.remove(user_requsted.pk)
    current_user_table.save()
    log(request.user.id,"CF")

    # add to the friends table of both sides.
    current_user_table = Friends.objects.filter(userid_id=request.user.id).first()
    current_user_table.myfriends.append(user_requsted.pk)
    user_confirm = Friends.objects.filter(userid_id=user_requsted.pk).first()
    user_confirm.myfriends.append(request.user.id)

    current_user_table.save()
    user_confirm.save()

def posts_user_liked(user_id):
    posts = Post.objects.all()
    liked_posts = []
    for p in posts:
        if p.likes.filter(id=user_id).values_list('likes', flat=True).first() is not None:
            post_i_liked = p.likes.filter(id=user_id).values_list('likes', flat=True).first()
            liked_posts.append(post_i_liked)
    return liked_posts

# helping for friend managment:

    # get in instance of the current user list of friend req
def myreqest(id):
    my_req_list = []
    friend_req = list(set(Friend_req.objects.all()))
    for i in friend_req:
        if id in i.myfriends_req:
            my_req_list.append(i.userid_id)
    return my_req_list



'''
this function will be track about the users operaions on the specific rounds.
the operations: 
1. AF (Add Friend)
2. CF (Confirm Friend)
3. LP (Like Post)
4. CP (Create Post)
5. P (Pass)
'''
def log(id_user,code_operation):
    all_rounds = Round.objects.all()
    current_round = Round.objects.filter(round_number=len(all_rounds)).first()
    print(f'Round for the LOG = {current_round.round_number}')
    l = Log(id_round=current_round.round_number,id_user=id_user,code_operation=code_operation)
    l.save()


# -------------------------------- Functions for Agent --------------------------------- #



def create_post_Agent(request):
    if request.method == 'POST':
       user_post_option = request.content_params['user_option']
       user_post_name = request.user
       pick = Status.objects.get(status = user_post_option)
       new_post = Post(username = user_post_name ,status = pick)
       new_post.save()
       log(request.user.id,"CP")
    return redirect('/ready')


def home_Agent(request):
    if request.method == 'POST':
       user_post_option = request.content_params['user_option_on_feed'] 
       user_post_name = request.user
       pick = Status.objects.get(status = user_post_option)
       new_post = Post(username = user_post_name ,status =pick)
       new_post.save()
       log(request.user.id,"CP")
    return redirect('/ready')



def like_post_Agent(request):
    if request.method == 'POST':
        post_like_id = request.content_params['post_id']
        post_like_id = Post.objects.get(id=post_like_id)
        post_like_id.likes.add(request.user)
        log(request.user.id,"LP")
    return redirect('/ready')

