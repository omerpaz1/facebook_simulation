from django.shortcuts import render,redirect    
import logging
from django.contrib.auth.signals import user_logged_in,user_logged_out,user_login_failed
from django.contrib.auth import authenticate, login
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import AllLogin,Users_free

# Create your views here.


logger = logging.getLogger(__name__)

dic = {
        2 : "facebookA1234",
        3 : "facebookB1234",
        4 : "facebookC1234",
        5 : "facebookD1234",
        6 : "facebookE1234",
        7 : "facebookF1234",
        8 : "facebookG1234",
        9 : "facebookH1234",
        10: "facebookI1234",

}

def info(request):
    if request.method == "POST":
        return redirect('/waiting')

    return render(request,'users/info.html')


def welcome(request):
    user_pick = -1
    pass_pick = -1
    if request.method == "POST":
        try:
            worker_id = request.POST.get('Worker_ID',False) 

            if len(worker_id) != 0:
                username , user_id, password = get_info(str(worker_id))
                is_valid = False
                context = {
                'user_pick' : username,
                'user_id' : user_id,
                }
                UserF = User.objects.filter(id=user_id).first()
                login(request,UserF)
                return redirect('/waiting')
            else:
                username = None
                password = None
                is_valid = True
        except:
            pass

    return render(request,'users/welcome.html')

# return user and password
def get_info(worker_id):
    Users_f = Users_free.objects.all()
    allusers = User.objects.all()
    userid = -1
    to_alocate = False
    for i in Users_f:
        if str(worker_id) == i.worker_id:
            userid = i.user_id
            pass_user = dic.get(userid) 
            username = allusers.filter(id=userid).first()
            return username , userid , pass_user

    if userid == -1:
        for i in Users_f:
            if i.worker_id == "None":
                alocate_user_id = i.user_id
                pass_user = dic.get(alocate_user_id) 
                username = allusers.filter(id=alocate_user_id).first()
                update_user = Users_free.objects.filter(user_id=alocate_user_id).first()
                update_user.worker_id = worker_id
                update_user.save()
                return username , alocate_user_id , pass_user


@receiver(user_logged_in)
def login_logger(sender, request, user,**kwargs):
    AllLogin.objects.create(user=request.user)
    return render(request,'facebook/waiting.html')

@receiver(user_logged_out)
def logout_logger(sender, request, user,**kwargs):
    AllLogin.objects.filter(user=request.user).delete()