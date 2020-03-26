from django.shortcuts import render , redirect
from .models import Post,Status
from django.contrib.auth.models import User
from django.views.generic import ListView,DeleteView,CreateView
from django.contrib.auth.decorators import login_required
import time



@login_required
def home(request):
    context = {
        'posts' : Post.objects.order_by('-date_posted'),
        'mystatus' : Status.objects.all()
    }
    if request.method == 'POST':
       user_post_option = request.POST.get('user_option_on_feed',False) 
       user_post_name = request.user
       pick = Status.objects.get(status_1 = user_post_option)
    # helping to see the values:   print(f'my pick is: {pick} , and username: {user_post_name}')
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
    # helping to see the values:   print(f'my pick is: {pick} , and username: {user_post_name}')
       new_post = Post(username = user_post_name ,status =user_post_option)
       new_post.save()
       return redirect('/home')
    else:
        return render(request,'facebook/post_form.html',context)
        
def create_post_from_feed(request):
    context = {
        'mystatus' : Status.objects.all(),
    }



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

