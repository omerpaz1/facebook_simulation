from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):
        return self.user.username

class AllLogin(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return str(self.user) + ': ' + str(self.date)

class Users_free(models.Model):
    worker_id = models.CharField(max_length=100,default="None")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # is_gived = models.BooleanField(default=False)

