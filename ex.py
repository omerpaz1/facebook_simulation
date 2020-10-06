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



if __name__ == '__main__':
    user_liked = posts_user_liked(3)
    print(user_liked)