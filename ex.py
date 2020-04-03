import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import Post,Status,Friends,Friend_req
from django.contrib.auth.models import User

posts = Post.objects.all()
liked_posts = []
for p in posts:
    if p.likes.filter(id=2).values_list('likes', flat=True).first() is not None:
        post_i_liked = p.likes.filter(id=2).values_list('likes', flat=True).first()
        liked_posts.append(post_i_liked)

print(liked_posts)
