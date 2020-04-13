import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import Post,Status,Friends,Friend_req
from django.contrib.auth.models import User


posts = Post.objects.all()
mystatus = Status.objects.all()
for p in posts:
        if p.status.has_link:
            print(p.status)

