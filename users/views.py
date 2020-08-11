from django.shortcuts import render,redirect    
import logging
from django.contrib.auth.signals import user_logged_in,user_logged_out,user_login_failed
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

}

def welcome(request):

    allusers = User.objects.all()
    Users_f = Users_free.objects.all()
    if request.method == "POST":
        # add alert if not pull
        # else go to login
        return redirect('/login')
    return render(request,'users/welcome.html')

def pull_userPass(request):
    user_pick = -1
    pass_pick = -1
    if request.method == "POST":
        worker_id = request.POST.get('Worker_ID',False) 
        username , user_id, password , to_alocate = get_info(worker_id)

        if to_alocate == True:
            update_user = Users_free.objects.filter(user_id=user_id).first()
            update_user.worker_id = worker_id
            update_user.save()
            user_pick = username
            pass_pick = password
        else:
            user_pick = 123
            pass_pick = 123


    context = {
            'user_pick' : user_pick,
            'pass_pick' : pass_pick,
    }
    return render(request,'users/welcome.html',context)

# return user and password
def get_info(worker_id):
    Users_f = Users_free.objects.all()
    allusers = User.objects.all()
    userid = -1
    to_alocate = False    ########################3snir
    for i in Users_f:
        if worker_id == i.worker_id:
            userid = i.user_id
            pass_user = dic.get(userid) 
            username = allusers.filter(id=userid).first()
            to_alocate = False
            return username , userid , pass_user , to_alocate

    if userid == -1:
        for i in Users_f:
            if i.worker_id == None:
                alocate_user_id = i.user_id
                pass_user = dic.get(alocate_user_id) 
                username = allusers.filter(id=alocate_user_id).first()
                to_alocate = True
                return username , alocate_user_id , pass_user , to_alocate


@receiver(user_logged_in)
def login_logger(sender, request, user,**kwargs):
    AllLogin.objects.create(user=request.user)
    return render(request,'facebook/waiting.html')

@receiver(user_logged_out)
def logout_logger(sender, request, user,**kwargs):
    AllLogin.objects.filter(user=request.user).delete()