import os
import django
import simulator
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
    all_rounds = Round.objects.all()
    new_round = Round(round_number=len(all_rounds)+1,posts_id=[],likes_id=[])
    new_round.save()
    current_round = Round.objects.filter(round_number=len(all_rounds)).first()
    # take all the posts id
    all_posts = Post.objects.all()
    all_likes = Post.likes.through.objects.all()

    posts_list = []
    for p in all_posts:
        posts_list.append(p.id)

    new_posts = get_new_posts(all_posts,all_rounds,current_round) 
    new_likes = get_new_likes(all_likes,all_rounds,current_round)

    for i in new_posts:
        new_round.posts_id.append(i)
    new_round.save()

    for i in new_likes:
        new_round.likes_id.append(i)
    new_round.save()

    print(f'round number: {new_round.round_number} , posts_id_list = {new_round.posts_id} , likes_id_list = {new_round.likes_id}')
    # ---------------------
    # take all the likes id
    # likes = posts_user_liked(user_id)
    # ---------------------


def get_new_posts(all_posts,all_rounds,current_round):
    new_posts = []
    for post in all_posts:
        flag = True
        for r_i in all_rounds:
            if post.id in r_i.posts_id:
                flag = False
                break
        if flag:
            new_posts.append(post.id)

    return new_posts

def get_new_likes(all_likes,all_rounds,current_round):
    new_likes = []
    for like in all_likes:
        flag = True
        for r_i in all_rounds:
            if like.pk in r_i.likes_id:
                flag = False
                break
        if flag:
            new_likes.append(like.pk)
    return new_likes

def my_likes_on_LC(LC,all_rounds,current_round):
    count_round = current_round.round_number
    if count_round < LC:
        start_LC = 0
    else:
        start_LC = count_round - LC
    
    end_LC = count_round
    print(f"Start = {start_LC}")
    print(f"end = {end_LC}")



if __name__ == '__main__':
    # simulator.simulator()
    # all_likes = Post.likes.through.objects.all()
    # for l in all_likes:
    #     print(l.pk)
    all_rounds = Round.objects.all()
    current_round = Round.objects.filter(round_number=len(all_rounds)).first()
    my_likes_on_LC(LC,all_rounds,current_round)