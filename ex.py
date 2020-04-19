import os
import django
import simulator
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import Post,Status,Friends,Friend_req,Round
from django.contrib.auth.models import User
import threading 
from facebook.views import posts_user_liked

LC = 3

def Post_on_feed(user_id):  
    add_posts_to_current_round(user_id)


def add_posts_to_current_round(user_id):
    new_round = Round(round_number=len(Round.objects.all())+1,posts_id=[],likes_id=[])
    new_round.save()
    all_rounds = Round.objects.all()
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
    no_likes_LC = likes_on_LC(user_id,LC,all_rounds,current_round,False)
    likes_LC = likes_on_LC(user_id,LC,all_rounds,current_round,True)

    for post in likes_LC:
        if post in no_likes_LC:
            no_likes_LC.pop(post)

    print(f'likes_LC = {likes_LC}')
    print(f'no_likes_LC = {no_likes_LC}')

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

def likes_on_LC(user_id,LC,all_rounds,current_round,like_post):
    user_likes_per_round = {}
    user_no_like_per_round = {}
    count_round = current_round.round_number
    if count_round < LC:  # 3 < 3? 
        start_LC = 1
    else:
        start_LC = count_round+1 - LC
    end_LC = count_round
    # get the current round start and end for the right LC rounds.
    start_round_LC = Round.objects.filter(round_number=(start_LC)).first()
    end_round_LC = Round.objects.filter(round_number=(end_LC)).first()

    begin = start_round_LC.round_number
    end = end_round_LC.round_number
    print(f'begin = {begin}')
    print(f'begin = {end}')

    LC_rounds = get_the_LC_rounds(begin,end)

    if like_post == True:
        for r_i in LC_rounds:
            for l_i in r_i.likes_id:
                if user_id == get_user_like_id(l_i):
                    user_likes_per_round.update({get_post_like_id(l_i) : r_i.round_number})
        return user_likes_per_round        
    if like_post == False:
        user_friends = Friends.objects.filter(userid_id=user_id).first().myfriends    
        for r_i in LC_rounds:
            for f_i in user_friends:
                posts_f_i = list(Post.objects.values_list('id', flat=True).filter(username_id=f_i))
                for p_i in  r_i.posts_id:
                    if p_i in posts_f_i:
                        user_no_like_per_round.update({p_i : -1})
        return user_no_like_per_round


# get the right rounds for the current LC rounds.
def get_the_LC_rounds(begin,end):
    LC_rounds = []
    for i in range(begin,end+1):
        round_i = Round.objects.filter(round_number=(i)).first()
        LC_rounds.append(round_i)
    return LC_rounds

# return the user_id of the current like_id
def get_user_like_id(like_id):
    all_likes = Post.likes.through.objects.all()
    for l_i in all_likes:
        if l_i.pk == like_id:
            return l_i.user_id

# return the current post_id of the like_id
def get_post_like_id(like_id):
    all_likes = Post.likes.through.objects.all()
    for l_i in all_likes:
        if l_i.pk == like_id:
            return l_i.post_id





if __name__ == '__main__':
    simulator.simulator()
    # all_likes = Post.likes.through.objects.all()
    # for l in all_likes:
    #     print(l.pk)
    # get_pk_per_like(60)
    # all_rounds = Round.objects.all()
    # current_round = Round.objects.filter(round_number=len(all_rounds)).first()
    # no_likes_LC = likes_on_LC(1,LC,all_rounds,current_round,False)
    # likes_LC = likes_on_LC(1,LC,all_rounds,current_round,True)

    # # for post in no_likes_LC:
    # #     if post in likes_LC:
    # #         likes_LC.pop(post)

    # print(f'likes_LC = {likes_LC}')
    # print(f'no_likes_LC = {no_likes_LC}')
    # p = list(Post.objects.values_list('id', flat=True).filter(username_id=3))
    # print(p)
    # list_a = {'omer' : 1 , 'snir' : 2}
    # list_b = {'yossi' : 1 , 'snir' : 2 ,'omer' : 1}

    # for x in list_a:
    #     if x in list_b:
    #         list_b.pop(x)

    # print(list_a)
    # print(list_b)

    
