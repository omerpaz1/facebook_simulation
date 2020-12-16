import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import *
from users.models import AllLogin,Users_free
from facebook.models import *
from facebook.views import *
from django.contrib.auth.models import User
import threading 
import math
from facebook.views import log
import facebook.algoritem as algo
from properties import *
import random
from timeit import default_timer as timer
import time
import itertools
import numpy
# from Util import toExel


#	               post | hasLink | Burden | Benefit| Privacy loss
posts={
    1  :	["I like Pizza", False, "0.2$", "0.5$", "0.1$"],
    2  :	["What is the meaning of life", False, "0.3$", "0.6$", "0.1$"],
    3  :	["Im tired of the cornavirus", False, "0.4$", "0.8$", "0.1$"],
    4  :	["If there is no flour eat cakes", False, "0.4$", "0.5$", "0.1$"],
    5  :	["Have a nice week", False, "0.2$", "0.3$", "0.1$"],
    6  :	["Im at the beach", False, "0.3$", "0.7$", "0.3$"],
    7  :	["Today, barbecue in the woods", False, "0.4$", "0.8$", "0.4$"],
    8  :	["Please help us www.cancer.com/Xf58b22", True, "0.6$", "0.8$", "0.2$"],
    9  : 	["In New York city", False, "0.4$", "0.6$", "0.2$"],
    10 :	["There was a crazy workout today", False, "0.7$", "0.5$", "0.1$"],
    11 :	["Help us find Max www.myDog.com/Pi10g71", True, "0.6$", "0.8$", "0.2$"],
    12 :	["The best burger www.BK.com/Mn47l84", True, "0.5$", "0.6$", "0.1$"],
    13 :	["NEWS www.Znet.com/Vj11w05", True, "0.4$", "0.9$", "0.1$"],
    14 :	["My cooking photo:)", False, "0.2$", "0.5$", "0.2$"],
    15 :	["Amazing song www.AC_DC.com/Yb12a24", True, "0.7$", "0.3$", "0.1$"],
    16 :	["I bought an apartment in Tel Aviv", False, "0.4$", "0.8$", "0.8$"],
    17 :	["Selling my guitar", False, "0.3$", "0.4$", "0.1$"],
    18 :	["The food industry is destroying the world", False, "0.3$", "0.8$", "0.2$"],
    19 :	["Meat is murder www.vegetables.com/Vg99j47", True, "0.8$", "0.5$", "0.3$"],
    20 :	["Here in Vegas", False, "0.2$", "0.7$", "0.4$"],
    21 :	["I lost weight :)", False, "0.2$", "0.6$", "0.3$"],
    22 :	["What is change ?!", False, "0.2$", "0.3$", "0.1$"],
    23 :	["Wanted waiter for www.MCdonalds.com/Kl46d12", True, "0.5$", "0.2$", "0.3$"],
    24 :	["Happy birthday to Liel 25!", False, "0.6$", "0.3$", "0.1$"],
    25 :	["Watching Game of Thrones tonight", False, "0.8$", "0.4$", "0.1$"],
    26 :	["Save the date www.married1/1/20.com/Uw00u51", True, "0.9$", "0.6$", "0.2$"],
    27 :	["Nail polish for $ 10", False, "0.5$", "0.2$", "0.2$"],
    28 :	["Look! a new haircut", False, "0.5$", "0.3$", "0.2$"],
    29 :	["funny vines www.youtube.com/Fu11y75", True, "0.6$", "0.8$", "0.2$"],
    30 :	["i hate emojis", False, "0.2$", "0.4$", "0.1$"]
}
PostsIUsed = {}


# def getStatusToPost(statusID):
#     status = Status.objects.filter(id=statusID).first().status
#     PostsIUsed.pop(statusID)
#     return status

if __name__ == '__main__':
    for key  in posts:
        s = Status.objects.filter(status=posts[key][0]).first()
        s.burden = posts[key][2]
        s.benefit = posts[key][3]
        s.PrivacyLoss = posts[key][4]
        s.sumWithOutBenefit =  float(s.benefit.replace('$', '')) - float(s.burden.replace('$', '')) -  float(s.PrivacyLoss.replace('$', ''))
        s.sumWithOutBenefit = round((s.sumWithOutBenefit),2)
        s.save()

        
    # key = max(PostsIUsed,key=PostsIUsed.get)
    # StatusToPost = getStatusToPost(key)
    # algo.UpdateScoreStatic(5)