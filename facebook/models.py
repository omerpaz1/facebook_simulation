from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField



# Post status options

status = 'I like Pizza'
status1 = 'Hello World'
status2 = 'What is coronavirus'
status3 = 'What is the meaning of life'

all_status = [
(status, 'I like Pizza'),
(status1, 'Hello World'),
(status2, 'What is coronavirus'),
(status3, 'What is the meaning of life'),
]

class Test(models.Model):
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    myfriends = ArrayField(
        ArrayField(
            models.IntegerField(),
            size=8,
        ),
        size=8,
    )

# end Post status options

class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=all_status,
        default='I like Pizza',
    )
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.status

class Status(models.Model):

    status_1 = models.CharField(max_length=50)

    PS = '0$'
    PS1 = '1$'
    PS2 = '2$'

    all_PS = [
        (PS, '0$'),
        (PS1, '1$'),
        (PS2, '2$'),

    ]
    PS = models.CharField(
        max_length=50,
        choices=all_PS,
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
        return self.status_1
