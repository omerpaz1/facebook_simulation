from .models import *
import random

LC = 10
BETWEEN_1_TO_2 = 0.4
BETWEEN_3_TO_5 = 0.2
BETWEEN_5_TO_LC = 0.1

leader_round_user_id = 1 # this user will be the last user that create new round

#puls 1 cuse range not include the end.
RANGE_PROB_BETWEEN_1_TO_2 = range(1,2+1)
RANGE_PROB_BETWEEN_3_TO_5 = range(3,5+1)
RANGE_PROB_BETWEEN_5_TO_LC = range(5,LC+1)

def Post_on_feed(user_id):  
    return add_posts_to_current_round(user_id)


def add_posts_to_current_round(user_id):
    new_round = -1
    if user_id == leader_round_user_id:
        new_round = Round(round_number=len(Round.objects.all())+1,posts_id=[],likes_id=[])
        new_round.save()
    
    all_rounds = Round.objects.all()
    new_round = Round.objects.filter(round_number=len(all_rounds)).first()
    # take all the posts id
    all_posts = Post.objects.all()
    all_likes = Post.likes.through.objects.all()

    posts_list = []
    for p in all_posts:
        posts_list.append(p.id)

    new_posts = get_new_posts(all_posts,all_rounds) 
    new_likes = get_new_likes(all_likes,all_rounds)
    for i in new_posts:
        print(i)
        new_round.posts_id.append(i)
    new_round.save()

    for i in new_likes:
        new_round.likes_id.append(i)
    new_round.save()

    print(f'round number: {new_round.round_number} , posts_id_list = {new_round.posts_id} , likes_id_list = {new_round.likes_id}')
    no_likes_LC = likes_on_LC(user_id,False)
    likes_LC = likes_on_LC(user_id,True)

    for post in likes_LC:
        if post in no_likes_LC:
            no_likes_LC.pop(post)

    print(f'likes_LC = {likes_LC}')
    print(f'no_likes_LC = {no_likes_LC}')

    return cal_prob(no_likes_LC,likes_LC)


def get_new_posts(all_posts,all_rounds):
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

def get_new_likes(all_likes,all_rounds):
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

def likes_on_LC(user_id,like_post):
    user_likes_per_round = {}
    user_no_like_per_round = {}

    LC_rounds = get_LC_rounds() # get the current rounds acording the LC

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
                        if f_i is user_id:
                            user_no_like_per_round.update({p_i : 0})
                        else: 
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


# return round number by given post id
def get_post_round(post_id):
    LC_rounds = get_LC_rounds()
    for r_i in LC_rounds:
        for p_i in r_i.posts_id:
            if p_i == post_id:
                return r_i.round_number




# return the current rounds for the LC
def get_LC_rounds():
    all_rounds = Round.objects.all()
    current_round = Round.objects.filter(round_number=len(all_rounds)).first()
    count_round = current_round.round_number
    if count_round < LC:  # 5 < 5? 
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
    print(f'end = {end}')

    LC_rounds = get_the_LC_rounds(begin,end)
    return LC_rounds



def cal_prob(no_likes_LC,likes_LC):
    posts_ans = []
    for post_no_liked in no_likes_LC: # about post with no like. same probability.
        if no_likes_LC[post_no_liked] == 0:
            posts_ans.append(post_no_liked)
        else:    
        # random number between [0,1]
            random_num = random.uniform(0,1)
            random_num = float('{0:.1f}'.format(random.uniform(0,1)))
            if random_num <= BETWEEN_5_TO_LC: # prob of 0.1
                posts_ans.append(post_no_liked)
    
    # for the post in the LC.
    for post_like in likes_LC:
        posted_round = get_post_round(post_like)
        liked_round = likes_LC[post_like]
        # LL not negative cuse like_round must be min 1 cuse no possible like and post i the same round
        LL = liked_round - posted_round
        # random number between [0,1]
        random_num = random.uniform(0,1)
        random_num = float('{0:.1f}'.format(random.uniform(0,1)))
        if LL in RANGE_PROB_BETWEEN_1_TO_2:
            if random_num <= BETWEEN_1_TO_2:
                posts_ans.append(post_like)
                # print(f' LL = {LL} , random_num <= BETWEEN_1_TO_2 -> {random_num}')
        elif LL in RANGE_PROB_BETWEEN_3_TO_5:
            if random_num <= BETWEEN_3_TO_5:
                posts_ans.append(post_like)
                # print(f' LL = {LL} , random_num <= BETWEEN_3_TO_5 -> {random_num}')
        elif LL in RANGE_PROB_BETWEEN_5_TO_LC:
            if random_num <= BETWEEN_5_TO_LC:
                posts_ans.append(post_like)
                # print(f' LL = {LL} , random_num <= RANGE_PROB_BETWEEN_5_TO_LC -> {random_num}')
    print(f"Posts picks = {posts_ans}")
    print("________________________end round________________________")
    return convert_posts(posts_ans)

# covert from post id to post object
def convert_posts(posts_LC):
    posts_as_querySet = []
    all_posts = Post.objects.all()
    for p in all_posts:
        if p.id in posts_LC:
            posts_as_querySet.append(p)
    return posts_as_querySet

    

'''
this function get a user posts on feed
return -> the possibole posts that he can like (not heis posts)
'''
def getOptionalLikePosts(user_id,current_posts):
    currentPostsOnFeed = getIdPosts(current_posts)
    OptionalLikePostsList = []
    no_likes_LC = likes_on_LC(user_id,False)
    for post in currentPostsOnFeed: # about post with no like. same probability.]
        if post in no_likes_LC:
            if no_likes_LC[post] == -1:
                OptionalLikePostsList.append(post)
    # convert_post(OptionalLikePostsList)
    return OptionalLikePostsList

'''
this function will get the users that know in your friend lists
it mean -> this users in the people you may know and you can ask for there friend.
return - > list if the users that you mayknow.
'''
def getPeopleMayKnow(user_id):
    PeopleMayKnow = []
    all_users = list(User.objects.values_list('id', flat=True)) 
    for _id in all_users:
        if _id != user_id:
            friends_req = list(Friend_req.objects.filter(userid_id=_id).first().myfriends_req)
            userFriends = list(Friends.objects.filter(userid_id=_id).first().myfriends)
            if user_id not in friends_req and user_id not in userFriends:
                PeopleMayKnow.append(_id)

    my_friends_req = getFriendsRequest(user_id)
    for i in PeopleMayKnow:
        if i in my_friends_req:
            PeopleMayKnow.remove(i)
    return PeopleMayKnow

'''
this function will return the list of user current requests
'''
def getFriendsRequest(user_id):
    return list(Friend_req.objects.filter(userid_id=user_id).first().myfriends_req)

'''
this function will return a status from all the status as a String that will be Posted.

'''

def getAllStatus():
    all_statuss = list(Status.objects.values_list('status', flat=True)) 
    return all_statuss


'''
this function will return all the ids posts from the rounds posts.
'''
def getIdPosts(round_posts):
    id_current_posts = []
    for i in round_posts:
        id_current_posts.append(i.id)
    return id_current_posts
