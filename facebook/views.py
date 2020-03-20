from django.shortcuts import render
from .models import Post
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    context = {
        'posts' : Post.objects.all()
    }
    return render(request,'facebook/feed.html',context)

@login_required
def create_post(request):
    return render(request,'facebook/create_post.html',{'title': 'create post'})