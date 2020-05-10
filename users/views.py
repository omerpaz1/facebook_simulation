from django.shortcuts import render
import logging
from django.contrib.auth.signals import user_logged_in,user_logged_out,user_login_failed
from django.dispatch import receiver
from .models import AllLogin

# Create your views here.


logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def login_logger(sender, request, user,**kwargs):
    AllLogin.objects.create(user=request.user)
    return render(request,'facebook/waiting.html')

@receiver(user_logged_out)
def logout_logger(sender, request, user,**kwargs):
    AllLogin.objects.filter(user=request.user).delete()