import os
import django
import ex
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import Post,Status,Friends,Friend_req,Round
from django.contrib.auth.models import User
import time 
from facebook.views import posts_user_liked

user_id = 2
UserA = 2
UserB = 3
UserC = 4
UserD = 5
UserE = 6

# userA -> friends : [UserB,UserC,UserD]
# userB -> friends : [UserA]
# userC -> friends : [UserA]
# userE -> friends : [UserD,UserB]
# userD -> friends : [UserA,UserE]

def simulator():
    # ------------------------- Round 1 -------------------------
    p_A_1 = Post(status_id=1,username_id=UserA) 
    p_B_1 = Post(status_id=1,username_id=UserB) 
    p_C_1 = Post(status_id=1,username_id=UserC)
    p_D_1 = Post(status_id=1,username_id=UserD)
    p_E_1 = Post(status_id=1,username_id=UserE)

    p_A_1.save()
    p_B_1.save()
    p_C_1.save()
    p_D_1.save()
    p_E_1.save()

    ex.Post_on_feed(user_id)
    # ------------------------- Round 2 -------------------------
    p_C_2 = Post(status_id=1,username_id=UserC)
    p_D_2 = Post(status_id=1,username_id=UserD)
    p_E_2 = Post(status_id=1,username_id=UserE)

    p_C_2.save()
    p_D_2.save()
    p_E_2.save()

    l_A2 = Post.likes.through(post_id=p_B_1.pk,user_id=UserA)
    l_B2 = Post.likes.through(post_id=p_A_1.pk,user_id=UserB)
    l_A2.save()
    l_B2.save()
    ex.Post_on_feed(user_id)
    # ------------------------- Round 3 -------------------------

    l_A3 = Post.likes.through(post_id=p_C_2.pk,user_id=UserA)
    l_C3 = Post.likes.through(post_id=p_A_1.pk,user_id=UserC)
    l_A3.save()
    l_C3.save()

    p_B_3 = Post(status_id=1,username_id=UserB) 
    p_E_3 = Post(status_id=1,username_id=UserE)        
    p_D_3 = Post(status_id=1,username_id=UserD)

    p_B_3.save()
    p_E_3.save()
    ex.Post_on_feed(user_id)
    # ------------------------- Round 4 -------------------------

    p_A_4 = Post(status_id=1,username_id=UserA) 
    p_B_4 = Post(status_id=1,username_id=UserB) 
    p_C_4 = Post(status_id=1,username_id=UserC)
    p_D_4 = Post(status_id=1,username_id=UserD)
    p_E_4 = Post(status_id=1,username_id=UserE)
    ex.Post_on_feed(user_id)

    # ------------------------- Round 5 -------------------------

    l_A5 = Post.likes.through(post_id=p_A_4.pk,user_id=UserA)
    l_A3.save()
    l_C3.save()
    ex.Post_on_feed(user_id)

