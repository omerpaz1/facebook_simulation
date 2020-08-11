import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import Post,Status,Friends,Friend_req,Round,Ready,WorkersInfo,Log
from users.models import AllLogin,Users_free
from django.contrib.auth.models import User
import threading 
from facebook.views import posts_user_liked
import random
import time


dic = {
        2 : "facebookA1234",
        3 : "facebookB1234",
        4 : "facebookC1234",
        5 : "facebookD1234",
        6 : "facebookE1234",

}

def get_info(worker_id):
    Users_f = Users_free.objects.all()
    allusers = User.objects.all()
    userid = -1
    to_alocate = False
    for i in Users_f:
        if worker_id == i.worker_id:
            userid = i.user_id
            pass_user = dic.get(userid) 
            username = allusers.filter(id=userid).first()
            to_alocate = False
            print("here")
            return username ,userid, pass_user , to_alocate

    if userid == -1:
        for i in Users_f:
            if i.worker_id == None:
                alocate_user_id = i.user_id
                pass_user = dic.get(alocate_user_id) 
                username = allusers.filter(id=alocate_user_id).first()
                update_user = Users_free.objects.filter(user_id=alocate_user_id).first()
                update_user.worker_id = worker_id
                update_user.save()
                to_alocate = True
                return username , alocate_user_id, pass_user , to_alocate

if __name__ == '__main__':
    username , alocate_user_id, pass_user , to_alocate = get_info()

    print(username)
    print(alocate_user_id)
    print(pass_user)
    print(to_alocate)

