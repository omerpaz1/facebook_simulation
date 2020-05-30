from django.shortcuts import render , redirect
from .models import Post,Status,Friends,Friend_req,Ready
from users.models import AllLogin
from django.contrib.auth.models import User
from django.views.generic import ListView,DeleteView,CreateView
from django.contrib.auth.decorators import login_required
import time
import facebook.algoritem as algo
import logging
import sys
from django.http import HttpRequest

Users_num = 3


def ready(request):
    Ready.objects.create(user=request.user) #create new Ready User
    users_ready = Ready.objects.all()
    set_users_ready = set()
    for i in users_ready:
        set_users_ready.add(i.user.id)
    users_ready = set_users_ready
    while(len(users_ready) < Users_num):
        users_ready = Ready.objects.all()
        for i in users_ready:
            set_users_ready.add(i.user.id)
        users_ready = set_users_ready
        context = {
            'ready_users' :users_ready,
            'allusers': User.objects.all(),
            'left_Users': Users_num-len(users_ready)
        }
        return render(request,'facebook/ready.html',context)    

    Ready.objects.all().delete()    
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

def ToCreate():
    pass

@login_required
def home(request):
    # posts = algo.Post_on_feed(request.user.id)

    user_liked = posts_user_liked(request.user.id)
    people_may_know = helper(request)
    list_friend_req = myreqest(request.user.id)
    

    context = {
        'posts' : Post.objects.order_by('-date_posted'),
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
       return redirect('/ready')

    return render(request,'facebook/feed.html',context)



@login_required
# function to create post
def create_post(request,user_option):
    print(request)
    context = {
        'mystatus' : Status.objects.all(),
        'posts' : Post.objects.all()
    }
    if request.method == 'POST':
    #    if not len(request.content_params):
    #         user_post_option = request.content_params['user_option']
    #         print("here!")
    #         print(f"{user_post_option}")
       user_post_option = request.POST.get('user_option',False)
       user_post_name = request.user
       pick = Status.objects.get(status = user_post_option)
       new_post = Post(username = user_post_name ,status = pick)
       new_post.save()
       return redirect('/ready')

    return render(request,'facebook/post_form.html',context)



    
# function when user click on the "like" btn.

def like_post(request):
    if request.method == 'POST':
        post_like_id = request.POST.get('post_id',False)
        post_like_id = Post.objects.get(id=post_like_id)
        post_like_id.likes.add(request.user)
    return redirect('/ready')




def manage_friends(request,operation,pk):
    print(pk)
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
                    friend_my_know.append(c_user)
    return friend_my_know
# user_requsted = the user that i want to add to my friends.

def addfriend(request ,user_requsted):
    print(f'requst = {request.user.id}')
    print(f'user_requsted = {user_requsted}')
    
    current_user = Friend_req.objects.filter(userid_id=request.user.id).first()
    if user_requsted.pk in current_user.myfriends_req: # if 3 in 5
        confirm_friends(request,user_requsted)
    else:
        user_requsted = Friend_req.objects.filter(userid_id=user_requsted.id).first()
        if current_user.userid_id not in user_requsted.myfriends_req:
            user_requsted.myfriends_req.append(request.user.id)
            user_requsted.save()

# comfirm both friend in the tables
def confirm_friends(request,user_requsted):
    current_user_table = Friend_req.objects.filter(userid_id=request.user.id).first()
    current_user_table.myfriends_req.remove(user_requsted.pk)
    current_user_table.save()

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




# check if all users auth.