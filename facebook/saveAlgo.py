from .models import *
import random
from properties import _benefit,_burden,_privacy_loss,total_rounds
from .models import Round,Status,Post,benefitRounds2
import threading
from . import views

LC = 10
adminUser = 1 # omerpaz user

BETWEEN_1_TO_2 =  0.4
BETWEEN_3_TO_5 =  0.2
BETWEEN_5_TO_LC =  0.1

from properties import agent_id
leader_round_user_id = agent_id # this user will be the last user that create new round

#puls 1 cuse range not include the end.
RANGE_PROB_BETWEEN_1_TO_2 = range(1,2+1)
RANGE_PROB_BETWEEN_3_TO_5 = range(3,5+1)
RANGE_PROB_BETWEEN_5_TO_LC = range(5,LC+1)

def Post_on_feed(user_id):
    posts = add_posts_to_current_round(user_id)
    UpDateScore(user_id,posts)
    return convert_posts(posts)


'''
this function will get all the information from the user_id and return the posts for the LC rounds.
'''
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
        new_round.posts_id.append(i)
    new_round.save()

    for i in new_likes:
        new_round.likes_id.append(i)
    new_round.save()
    print(f'----------------  # Start Round: {new_round.round_number} ----------------\n')
    print(f'posts_id_list = {new_round.posts_id} , likes_id_list = {new_round.likes_id}')
    no_likes_LC = likes_on_LC(user_id,False)
    likes_LC = likes_on_LC(user_id,True)

    for post in likes_LC:
        if post in no_likes_LC:
            no_likes_LC.pop(post)

    print(f'likes_LC = {likes_LC}')
    print(f'no_likes_LC = {no_likes_LC}')
    user_friends = Friends.objects.filter(userid_id=user_id).first().myfriends    
    return cal_prob(no_likes_LC,likes_LC,user_friends)


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
    user_friends = Friends.objects.filter(userid_id=user_id).first().myfriends    
    LC_rounds = get_LC_rounds() # get the current rounds acording the LC
    if like_post == True:
        for r_i in LC_rounds:
            for l_i in r_i.likes_id:
                member_id = get_user_like_id(l_i)
                if member_id in user_friends:
                    for j in LC_rounds:
                        if get_post_like_id(l_i) in j.posts_id:
                            user_likes_per_round.update({get_post_like_id(l_i) : r_i.round_number})
        return user_likes_per_round        
    if like_post == False:
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
    if count_round <= LC:  # 11 <= 10? 
        start_LC = 1  # 2 - 11 (11-1)
    else:
        start_LC = count_round - LC
    end_LC = count_round
    # get the current round start and end for the right LC rounds.

    start_round_LC = Round.objects.filter(round_number=(start_LC)).first()
    end_round_LC = Round.objects.filter(round_number=(end_LC)).first()
    begin = start_round_LC.round_number
    end = end_round_LC.round_number
    LC_rounds = get_the_LC_rounds(begin,end)
    return LC_rounds


def getMaxLL(likes_LC,no_likes_LC,friend_id):
    minLL = 1000
    tempPosts = []
    for post_like in likes_LC:
        all_likes = Post.likes.through.objects.all()

        for like in all_likes:
            if like.post_id == post_like and like.user_id == friend_id:
                tempPosts.append(post_like)
        
        for p in tempPosts:
            posted_round = get_post_round(p)
            liked_round = likes_LC[p]
            try:
                LL = (liked_round-1) - (posted_round-1)
            except:
                pass
            if LL < minLL:
                print(liked_round-1,posted_round-1)
                print(p)
                print(f'minLL was:{minLL}')
                minLL = LL
                print(f'minLL now:{minLL}')
    return minLL, tempPosts


def cal_prob(no_likes_LC,likes_LC,user_friends):
    posts_ans = []
    for post_no_liked in no_likes_LC: # about post with no like. same probability.
        if no_likes_LC[post_no_liked] == 0:
            posts_ans.append(post_no_liked)
    
    # for the post in the LC.
    for friend_id in user_friends:

        LL, tempPosts  = getMaxLL(likes_LC,no_likes_LC,friend_id)

        for post_like in tempPosts:
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
        print(f"Posts picks = {posts_ans}\n")
    return posts_ans

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
    Optional_SAFE_LikePostsList = []
    Optional_UN_SAFE_LikePostsList = []
    no_likes_LC = likes_on_LC(user_id,False)
    for key,value in no_likes_LC.items(): # about post with no like. same probability.]
        if key in currentPostsOnFeed:
            if value == -1:
                post = Post.objects.filter(id=key).first()
                post_i_liked = post.likes.filter(id=user_id).values_list('likes', flat=True).first()
                if post_i_liked != None:
                    continue
                status =  Status.objects.filter(id=post.status_id).first()
                if status.has_link:
                    Optional_UN_SAFE_LikePostsList.append(key)
                else:
                    Optional_SAFE_LikePostsList.append(key)
    return Optional_SAFE_LikePostsList,Optional_UN_SAFE_LikePostsList

'''
this function will get the users that know in your friend lists
it mean -> this users in the people you may know and you can ask for there friend.
return - > list if the users that you mayknow.
'''
def getPeopleMayKnow(user_id):
    PeopleMayKnow = []
    all_users = list(User.objects.values_list('id', flat=True))
    all_users.remove(adminUser)
    for _id in all_users:
        if _id != user_id:
            friends_req = list(Friend_req.objects.filter(userid_id=_id).first().myfriends_req)
            userFriends = list(Friends.objects.filter(userid_id=user_id).first().myfriends)
            if user_id not in friends_req and _id not in userFriends:
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



'------------------------- Score ---------------------'

def getUserByRound(argument,postUserID,PostID): 
    userBene = benefitRounds2.objects.filter(id_user=postUserID).first()
    if argument == 1:
        userBene.round_1.append(PostID)
        userBene.save()
    elif argument == 2:
        userBene.round_2.append(PostID)
        userBene.round_2=set(userBene.round_2)
        userBene.round_2=list(userBene.round_2)
        userBene.save()
    elif argument == 3:
        userBene.round_3.append(PostID)
        userBene.round_3=set(userBene.round_3)
        userBene.round_3=list(userBene.round_3)
        userBene.save()
    elif argument == 4:
        userBene.round_4.append(PostID)
        userBene.round_4=set(userBene.round_4)
        userBene.round_4=list(userBene.round_4)
        userBene.save()
    elif argument == 5:
        userBene.round_5.append(PostID)
        userBene.round_5=set(userBene.round_5)
        userBene.round_5=list(userBene.round_5)
        userBene.save()
    elif argument == 6:
        userBene.round_6.append(PostID)
        userBene.round_6=set(userBene.round_6)
        userBene.round_6=list(userBene.round_6)
        userBene.save()
    elif argument == 7:
        userBene.round_7.append(PostID)
        userBene.round_7=set(userBene.round_7)
        userBene.round_7=list(userBene.round_7)
        userBene.save()
    elif argument == 8:
        userBene.round_8.append(PostID)
        userBene.round_8=set(userBene.round_8)     
        userBene.round_8=list(userBene.round_8)           
        userBene.save()
    elif argument == 9:
        userBene.round_9.append(PostID)
        userBene.round_9=set(userBene.round_9)
        userBene.round_9=list(userBene.round_9)
        userBene.save()
    elif argument == 10:
        userBene.round_10.append(PostID)
        userBene.round_10=set(userBene.round_10)
        userBene.round_10=list(userBene.round_10)
        userBene.save()
    elif argument == 11:
        userBene.round_11.append(PostID)
        userBene.round_11=set(userBene.round_11)
        userBene.round_11=list(userBene.round_11)
        userBene.save()
    elif argument == 12:
        userBene.round_12.append(PostID)
        userBene.round_12=set(userBene.round_12)
        userBene.round_12=list(userBene.round_12)
        userBene.save()
    elif argument == 13:
        userBene.round_13.append(PostID)
        userBene.round_13=set(userBene.round_13)
        userBene.round_13=list(userBene.round_13)
        userBene.save()
    elif argument == 14:
        userBene.round_14.append(PostID)
        userBene.round_14=set(userBene.round_14)
        userBene.round_14=list(userBene.round_14)
        userBene.save()
    elif argument == 15:
        userBene.round_15.append(PostID)
        userBene.round_15=set(userBene.round_15)
        userBene.round_15=list(userBene.round_15)
        userBene.save()

def UpDateScore(user_id,CurrentPostsOnRound):
    for p in CurrentPostsOnRound:
        roundNumber = int(len(Round.objects.all()))
        post = Post.objects.filter(id=p).first()
        if post.username_id != user_id:
            getUserByRound(roundNumber,post.username_id,p)


def getRoundList(argument,postUserID): 
    userBene = benefitRounds2.objects.filter(id_user=postUserID).first()
    dic = {
    1:userBene.round_1,
    2: userBene.round_2,
    3: userBene.round_3,
    4: userBene.round_4,
    5: userBene.round_5,
    6: userBene.round_6,
    7: userBene.round_7,
    8: userBene.round_8,
    9: userBene.round_9,
    10: userBene.round_10,
    11: userBene.round_11,
    12: userBene.round_12,
    13: userBene.round_13,
    14: userBene.round_14,
    15: userBene.round_15
    }
    return dic.get(argument)


'''
this function will get the user that need to update heis score by showing heis post on the feed.
will update heis Benefits Row.
'''



'''
this function will update the score of user by static values that given on heis operation.(like,add friend etc..)
'''
def UpdateScoreStatic(userID_ToUpdate):
    userScore = Score.objects.filter(id_user=userID_ToUpdate).first()
    logs = Log.objects.all()
    for i in logs:
        if i.id_user == userID_ToUpdate:
            if i.code_operation == "P":
                burden_val,privacy_loss_val = UpDateScoreForLikes(i.post_id)
                userScore.burden = userScore.burden + burden_val
                userScore.privacy_loss = userScore.privacy_loss + privacy_loss_val
            elif i.code_operation == "AF":
                userScore.burden = userScore.burden + 0.6
            elif i.code_operation == "OF":
                userScore.burden = userScore.burden + 1.2
            elif i.code_operation == "SL":
                burden_val,privacy_loss_val = UpDateScoreForLikes(i.post_id)
                userScore.burden = userScore.burden + burden_val
                userScore.privacy_loss = userScore.privacy_loss + privacy_loss_val
            elif i.code_operation == "UL":
                burden_val,privacy_loss_val = UpDateScoreForLikes(i.post_id)
                userScore.burden = userScore.burden + burden_val
                userScore.privacy_loss = userScore.privacy_loss + privacy_loss_val

            userScore.benefit = UpdateScoreForPosts(i.id_user)
    userScore.final_score = userScore.burden + userScore.benefit - userScore.privacy_loss
    print(f"userScore.privacy_loss = {userScore.privacy_loss}, userScore.burden = {userScore.burden} , userScore.benefit = {userScore.benefit}")
    userScore.save()

def UpdateScoreForPosts(user_id):
    benefit_val = 0
    burden_val = 0
    privacy_loss_val = 0

    beneUsers = benefitRounds2.objects.all()
    for i in range(1,total_rounds+1):
        array = getRoundList(i,user_id)
        if array:
            for postID in array:
                statusID = Post.objects.get(id=postID).status_id
                status_info =  Status.objects.filter(id=statusID).first()
                benefit_val+= float(status_info.benefit.replace('$', ''))

    return round((benefit_val),2)

def UpDateScoreForLikes(post_id):
    burden_val = 0
    privacy_loss_val = 0

    statusID = Post.objects.get(id=post_id).status_id
    status_info =  Status.objects.filter(id=statusID).first()
    burden_val = float(status_info.burden.replace('$', ''))
    privacy_loss_val = float(status_info.PrivacyLoss.replace('$', ''))
    return round((burden_val),2),round((privacy_loss_val),2)

    0