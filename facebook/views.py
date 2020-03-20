from django.shortcuts import render
from .models import Post


def home(request):
    context = {
        'posts' : Post.objects.all()
    }
    return render(request,'facebook/post.html',context)


def create_first_post(request):
    return render(request,'facebook/create_first_post.html',{'title': 'create post'})