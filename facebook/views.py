from django.shortcuts import render , redirect
from .models import Post,Status,Friends,Friend_req
from django.contrib.auth.models import User
from django.views.generic import ListView,DeleteView,CreateView
from django.contrib.auth.decorators import login_required
import time
import logging
import sys

list_friend_req_O = []
list_friend_req_A = []
list_friend_req_B = []
list_friend_req_C = []
list_friend_req_D = []

@login_required
def home(request):    
    user_liked = posts_user_liked(request)
    people_my_know = helper(request)
    list_friend_req = myreq(request.user.id)
    print(f"list_friend_req = {list_friend_req}")

    context = {
        'posts' : Post.objects.order_by('-date_posted'),
        'mystatus' : Status.objects.all(),
        'friends' : Friends.objects.filter(userid_id=request.user.id).first().myfriends,
        'friends_requst' : list(set(Friend_req.objects.filter(userid_id=request.user.id).first().myfriends_req)),
        'people_my_know' : people_my_know,
        'users' : User.objects.all(),
        'posts_user_liked' : user_liked,
        'list_friend_req' : list_friend_req
    }
    if request.method == 'POST':
       user_post_option = request.POST.get('user_option_on_feed',False) 
       user_post_name = request.user
       pick = Status.objects.get(status_1 = user_post_option)
       new_post = Post(username = user_post_name ,status =user_post_option)
       new_post.save()
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
       pick = Status.objects.get(status_1 = user_post_option)
       new_post = Post(username = user_post_name ,status =user_post_option)
       new_post.save()
       return redirect('/home')
    else:
        return render(request,'facebook/post_form.html',context)
    
# function when user click on the "like" btn.

def like_post(request):
    if request.method == 'POST':
        post_like_id = request.POST.get('post_id',False)
        post_like_id = Post.objects.get(id=post_like_id)
        post_like_id.likes.add(request.user)
    return redirect('/home')




def manage_friends(request,operation,pk):
    print(pk)
    user_requsted = User.objects.get(pk=pk)
    if operation =='friend_requset':
        addfriend(request,user_requsted)
    if operation == 'friend_confirm':
        confirm_friends(request,user_requsted)
    return redirect('/home')


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
    list_current_friend_req = myreq(request.user.id)
    
    current_user = Friend_req.objects.filter(userid_id=request.user.id).first()
    if user_requsted.pk in current_user.myfriends_req: # if 3 in 5
        confirm_friends(request,user_requsted)
    else:
        user_requsted = Friend_req.objects.filter(userid_id=user_requsted.id).first()
        if current_user.userid_id not in user_requsted.myfriends_req:
            list_current_friend_req.append(user_requsted.userid_id) # adding to list of user requsted
            user_requsted.myfriends_req.append(request.user.id)
            user_requsted.save()

# comfirm both friend in the tables
def confirm_friends(request,user_requsted):
    list_current_friend_req = myreq(user_requsted.pk)
    current_user_table = Friend_req.objects.filter(userid_id=request.user.id).first()
    current_user_table.myfriends_req.remove(user_requsted.pk)
    current_user_table.save()

    # add to the friends table of both sides.
    current_user_table = Friends.objects.filter(userid_id=request.user.id).first()
    current_user_table.myfriends.append(user_requsted.pk)
    user_confirm = Friends.objects.filter(userid_id=user_requsted.pk).first()
    user_confirm.myfriends.append(request.user.id)
    list_current_friend_req.remove(current_user_table.userid_id)

    current_user_table.save()
    user_confirm.save()

def posts_user_liked(request):
    posts = Post.objects.all()
    liked_posts = []
    for p in posts:
        if p.likes.filter(id=1).values_list('likes', flat=True).first() is not None:
            post_i_liked = p.likes.filter(id=request.user.id).values_list('likes', flat=True).first()
            liked_posts.append(post_i_liked)
    return liked_posts


    # get in instance of the current user list of friend req
def myreq(id):
    if id == 1:
        return list_friend_req_O
    if id == 2:
        return list_friend_req_A
    if id == 3:
        return list_friend_req_B
    if id == 4:
        return list_friend_req_C
    if id == 5:
        return list_friend_req_D