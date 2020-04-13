from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField



# Post status options

status = 'I like Pizza'
status1 = 'Hello World'
status2 = 'What is coronavirus www.coronavirus.com'
status3 = 'What is the meaning of life'

all_status = [
(status, status),
(status1, status1),
(status2, status2),
(status3, status3),
]

class Friends(models.Model):
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    myfriends = ArrayField(
        ArrayField(
            models.IntegerField(),
            size=8,
        ),
        size=8,
    )

class Friend_req(models.Model):
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    myfriends_req = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True),size=8,),size=8,)

# end Post status options


class Status(models.Model):

    status = models.CharField(max_length=50,choices=all_status,default='I like Pizza',)
    has_link = models.BooleanField(default=False)

    PrivacyLoss = '0$'
    PrivacyLoss1 = '1$'
    PrivacyLoss2 = '2$'

    all_PrivacyLoss = [
        (PrivacyLoss, '0$'),
        (PrivacyLoss1, '1$'),
        (PrivacyLoss2, '2$'),

    ]
    PrivacyLoss = models.CharField(
        max_length=50,
        choices=all_PrivacyLoss,
        default='0$',
    )

    burden = '0$'
    burden1 = '1$'
    burden2 = '2$'
    
    all_burden = [
        (burden, '0$'),
        (burden1, '1$'),
        (burden2, '2$'),

    ]
    burden = models.CharField(
        max_length=50,
        choices=all_burden,
        default='0$',
    )

    benefit = '0$'
    benefit1 = '1$'
    benefit2 = '2$'
    
    all_benefit = [
        (benefit, '0$'),
        (benefit1, '1$'),
        (benefit2, '2$'),

    ]
    benefit = models.CharField(
        max_length=50,
        choices=all_benefit,
        default='0$',
    )
    def __str__(self):
        return self.status

class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User,related_name='likes',blank=True)
    
    def __str__(self):
        return str(self.status)
    
    def total_likes(self):
        return self.likes.count()