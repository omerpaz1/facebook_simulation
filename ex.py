import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import Post,Status,Friends,Friend_req
from django.contrib.auth.models import User
import threading 


def gfg(): 
    print("GeeksforGeeks\n") 
  
timer = threading.Timer(10.0, gfg) 
timer.start() 
print("Exit\n") 

