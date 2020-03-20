from django.shortcuts import render
from .models import Post
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    context = {
        'posts' : Post.objects.all()
    }
    return render(request,'facebook/post.html',context)

@login_required
def create_first_post(request):
    return render(request,'facebook/create_first_post.html',{'title': 'create post'})