from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
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
    status = models.CharField(
        max_length=50,
        choices=all_status,
        default='I like Pizza',
    )
    # status = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.status