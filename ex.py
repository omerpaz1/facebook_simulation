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
import RandomActions as RA
def getRandomOpeartion2Players(data):
    random.shuffle(data)
    return data[0][0],data[0][1]

def getChlids(po):
    anslist = []
    mylist = []
    for o in po:
        l = []
        for key,value in o.items():
            l.append(key)
        mylist.append(l)

    for element in itertools.product(*mylist):
        anslist.append(element)
    return anslist

if __name__ == '__main__':
    random_num = random.uniform(0,1)
    random_num = float('{0:.1f}'.format(random.uniform(0,1)))
    print(random_num)