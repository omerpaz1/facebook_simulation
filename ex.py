import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import Post,Status,Friends,Friend_req,Round,Ready,WorkersInfo,Log,Score,benefitRounds
from users.models import AllLogin,Users_free
from django.contrib.auth.models import User
import threading 
import math
from facebook.views import posts_user_liked
import facebook.algoritem as algo
from properties import adminUser,agent_id,_benefit,_burden,_privacy_loss
import random
import time


def getRoundList(argument,postUserID): 
    userBene = benefitRounds.objects.filter(id_user=postUserID).first()
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

total_rounds = 15

def UpdateScoreForPosts(user_id):
    benefit_val = 0
    burden_val = 0
    privacy_loss_val = 0

    beneUsers = benefitRounds.objects.all()
    for i in range(1,total_rounds+1):
        array = getRoundList(i,user_id)
        if array:
            for postID in array:
                statusID = Post.objects.get(id=postID).status_id
                status_info =  Status.objects.filter(id=statusID).first()
                benefit_val+= float(status_info.benefit.replace('$', ''))
                burden_val+= float(status_info.burden.replace('$', ''))
                privacy_loss_val+= float(status_info.PrivacyLoss.replace('$', ''))

    print(round((benefit_val),2),round((burden_val),2),round((privacy_loss_val),2))
    return round((benefit_val),2),round((burden_val),2),round((privacy_loss_val),2)


def UpdateScoreStatic(userID_ToUpdate):
    userScore = Score.objects.filter(id_user=userID_ToUpdate).first()
    logs = Log.objects.all()
    for i in logs:
        if i.id_user == userID_ToUpdate:
            if i.code_operation == "P":
                benefit_val,burden_val,privacy_loss_val = UpdateScoreForPosts(i.id_user)
                userScore.burden = userScore.burden + burden_val
                userScore.privacy_loss = userScore.privacy_loss + privacy_loss_val
            elif i.code_operation == "AF":
                userScore.burden = userScore.burden + _burden
            elif i.code_operation == "OF":
                userScore.burden = userScore.burden + _burden
            elif i.code_operation == "SL":
                burden_val,privacy_loss_val = UpDateScoreForLikes(i.post_id)
                userScore.burden = userScore.burden + burden_val
                userScore.privacy_loss = userScore.privacy_loss + privacy_loss_val
            elif i.code_operation == "UL":
                burden_val,privacy_loss_val = UpDateScoreForLikes(i.post_id)
                userScore.burden = userScore.burden + burden_val
                userScore.privacy_loss = userScore.privacy_loss + privacy_loss_val
    userScore.final_score = userScore.final_score + userScore.privacy_loss + userScore.burden + userScore.benefit
    print(userScore.final_score)
    # userScore.save()

def UpdateScoreForPosts(user_id):
    benefit_val = 0
    burden_val = 0
    privacy_loss_val = 0

    beneUsers = benefitRounds.objects.all()
    for i in range(1,total_rounds+1):
        array = getRoundList(i,user_id)
        if array:
            for postID in array:
                statusID = Post.objects.get(id=postID).status_id
                status_info =  Status.objects.filter(id=statusID).first()
                benefit_val+= float(status_info.benefit.replace('$', ''))
                burden_val+= float(status_info.burden.replace('$', ''))
                privacy_loss_val+= float(status_info.PrivacyLoss.replace('$', ''))

    # print(round((benefit_val),2),round((burden_val),2),round((privacy_loss_val),2))
    return round((benefit_val),2),round((burden_val),2),round((privacy_loss_val),2)

def UpDateScoreForLikes(post_id):
    burden_val = 0
    privacy_loss_val = 0

    statusID = Post.objects.get(id=1756).status_id
    status_info =  Status.objects.filter(id=statusID).first()
    burden_val+= float(status_info.burden.replace('$', ''))
    privacy_loss_val+= float(status_info.PrivacyLoss.replace('$', ''))
    return round((burden_val),2),round((privacy_loss_val),2)


if __name__ == '__main__':
    UpdateScoreStatic(2)
