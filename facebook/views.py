from django.shortcuts import render
from .models import Post
from django.views.generic import ListView,DeleteView,DetailView,CreateView
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    context = {
        'posts' : Post.objects.all()
    }
    return render(request,'facebook/feed.html',{'title': 'feed'})

@login_required
def create_post(request):
    return render(request,'facebook/post_form.html',{'title': 'create post'})


class PostListView(ListView):
    model = Post
    template_name  = 'facebook/feed.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

class PostCreateView(CreateView):
    model = Post
    fields = ['username','status']