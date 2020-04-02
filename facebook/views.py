from django.shortcuts import render , redirect
from .models import Post,Status,Friends,Friend_req
from django.contrib.auth.models import User
from django.views.generic import ListView,DeleteView,CreateView
from django.contrib.auth.decorators import login_required
import time
import logging
import sys


textvalue = "its a Test"


@login_required
def home(request):    
    people_my_know = helper(request)
    context = {
        'posts' : Post.objects.order_by('-date_posted'),
        'mystatus' : Status.objects.all(),
        'friends' : Friends.objects.filter(userid_id=request.user.id).first().myfriends,
        'friends_requst' : list(set(Friend_req.objects.filter(userid_id=request.user.id).first().myfriends_req)),
        'people_my_know' : people_my_know,
        'users' : User.objects.all()
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

def like_post(request):
    if request.method == 'POST':
        post_like_id = request.POST.get('post_id',False)
        post_like_id = Post.objects.get(id=post_like_id)
        post_like_id.likes.add(request.user)
    return redirect('/home')




def manage_friends(request,operation,pk):
    user_requsted = User.objects.get(pk=pk)
    if operation =='friend_requset':
      print(f'friend_requset operation = {user_requsted}')
      current_user_table = Friend_req.objects.filter(userid_id=user_requsted.id).first()
      if request.user.id not in current_user_table.myfriends_req:
        current_user_table.myfriends_req.append(request.user.id)
        current_user_table.save()
    if operation == 'friend_confirm':
       # remove from Friend_requsts table the requset
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
