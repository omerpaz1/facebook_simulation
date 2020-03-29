from django.shortcuts import render , redirect
from .models import Post,Status,Friends,Friend_req
from django.contrib.auth.models import User
from django.views.generic import ListView,DeleteView,CreateView
from django.contrib.auth.decorators import login_required
import time



@login_required
def home(request):
    f = Friend_req.objects.filter(userid_id=request.user.id).first()
    f =list(set(f.myfriends_req))
    context = {
        'posts' : Post.objects.order_by('-date_posted'),
        'mystatus' : Status.objects.all(),
        'friends' : Friends.objects.filter(userid_id=request.user.id).first(),
        'friends_requst' : f,
        'users' : User.objects.all()
    }
    if request.method == 'POST':
       user_post_option = request.POST.get('user_option_on_feed',False) 
       user_post_name = request.user
       print(f'userid requset = {request.user.id}')
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
        
def manage_friends(request,operation,pk):
    user_requsted = User.objects.get(pk=pk)
        
    print(request.user.username)
    if operation =='friend_requset':
      current_user_table = Friend_req.objects.filter(userid_id=user_requsted.id).first()
      current_user_table.myfriends_req.append(request.user.id)
      current_user_table.save()
    if operation == 'friend_confirm':
       print(f'here! = {user_requsted}')
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









# list all the post in the home page

# class PostListView(ListView):
#     model = Post
#     template_name  = 'facebook/feed.html'
#     context_object_name = 'posts'
#     ordering = ['-date_posted']

#     def get_context_data(self, **kwargs):
#         context = super(PostListView, self).get_context_data(**kwargs)
#         context['mystatus'] =  Status.objects.all()

#         return context


# info of the current post

