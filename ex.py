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
import numpy
# from Util import toExel



if __name__ == '__main__':
    Users_num = 3
    users = User.objects.all().order_by('id')[1:4]
    for i in users:
        print(i ," id: ",i.id)
    # for i in reversed(range(Users_num+2,11)):
    #     print(i)