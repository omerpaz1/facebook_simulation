import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import Post,Status,Friends,Friend_req,Round
from django.contrib.auth.models import User
import threading 
from facebook.views import posts_user_liked

LC = 10

def Post_on_feed(user_id):  
    add_posts_to_current_round(user_id)


def add_posts_to_current_round(user_id):
    r = Round.objects.all()
    r = Round(round_number=len(r)+1,posts_id=[],likes_id=[])
    r.save()
    # take all the posts id
    all_posts = Post.objects.all()
    posts_list = []
    all_posts = Post.objects.all()
    for p in all_posts:
        posts_list.append(p.id)
    new_posts = get_new_posts(all_posts) 
    for i in new_posts:
        r.posts_id.append(i)
    r.save()

    print(f'round number: {r.round_number} , posts_id_list = {r.posts_id}')
    # ---------------------
    # take all the likes id
    # likes = posts_user_liked(user_id)
    # ---------------------


def get_new_posts(all_posts):
    new_posts = []
    all_rounds = Round.objects.all()
    current_round = Round.objects.filter(round_number=len(all_rounds)).first()
    for post in all_posts:
        flag = True
        for r_i in all_rounds:
            if post.id in r_i.posts_id:
                print(f"{post.id} all ready in the list!")
                flag = False
                break
        if flag:
            new_posts.append(post.id)

    return new_posts

        


def simulator():
    posts = Post.objects.all()
    # print(posts)        
    for p in posts:
        t = list(p.likes.values('id'))
        print(t)
    # p1 = Post(status_id=1,username_id=1)
    # p2 = Post(status_id=1,username_id=2)
    # p1.save()
    # p2.save()
    # Post_on_feed(1)
    # p3 = Post(status_id=2,username_id=3)
    # p4 = Post(status_id=2,username_id=4)
    # p3.save()
    # p4.save()
    # Post_on_feed(1)
    # p5 = Post(status_id=3,username_id=5)
    # p6 = Post(status_id=3,username_id=2)
    # p7 = Post(status_id=3,username_id=1)
    # p5.save()
    # p6.save()
    # p7.save()
    # Post_on_feed(1)     


if __name__ == '__main__':
    simulator()

