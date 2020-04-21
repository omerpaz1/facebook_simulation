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
    p1 = Post(status_id=1,username_id=1) # r1 = posts =[p1,p2,p3,p4] , likes = []
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
    l2 = Post.likes.through(post_id=p4.pk,user_id=2)
    l2.save()
    ex.Post_on_feed(1)
    # Round n3:
    p6 = Post(status_id=3,username_id=2) # r3 = posts =[p6] , likes = [L(p4)]
    p6.save()
    l3 = Post.likes.through(post_id=p4.pk,user_id=1)
    l3.save()
    ex.Post_on_feed(1)   
    # # Round n4:
    p7 = Post(status_id=4,username_id=3) # r4 = posts =[p7,p7] , likes = []
    p8 = Post(status_id=4,username_id=4)
    p7.save()
    p8.save()
    ex.Post_on_feed(1)   
    # # Round n5:
    p9 = Post(status_id=4,username_id=2) # r5 = posts =[p9] , likes = []
    p9.save()
    ex.Post_on_feed(1)  
    # # Round n6:
    p10 = Post(status_id=4,username_id=1) # r4 = posts =[p10] , likes = []
    p10.save()
    ex.Post_on_feed(1)   
    # # Round n7:
    l1 = Post.likes.through(post_id=p2.pk,user_id=1) # r2 = posts =[p5] , likes = [L(p2) , L(p4)]
    l1.save()
    ex.Post_on_feed(1)   



