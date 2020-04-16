import os
import django
import ex
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import Post,Status,Friends,Friend_req,Round
from django.contrib.auth.models import User
import threading 
from facebook.views import posts_user_liked




def simulator():
    # Round n1:
    p1 = Post(status_id=1,username_id=1)
    p2 = Post(status_id=1,username_id=2)
    p3 = Post(status_id=1,username_id=3)
    p4 = Post(status_id=1,username_id=4)
    p1.save()
    p2.save()
    p3.save()
    p4.save()
    ex.Post_on_feed(1)
    # Round n2:
    p5 = Post(status_id=2,username_id=3)
    p5.save()
    l1 = Post.likes.through(post_id=p2.pk,user_id=1)
    l2 = Post.likes.through(post_id=p4.pk,user_id=2)
    l1.save()
    l2.save()
    ex.Post_on_feed(1)
    # Round n3:
    p6 = Post(status_id=3,username_id=2)
    p6.save()
    l3 = Post.likes.through(post_id=p4.pk,user_id=1)
    l3.save()
    ex.Post_on_feed(1)     

