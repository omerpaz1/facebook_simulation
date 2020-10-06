from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField



# Post status options

status =	"I like pizza"
status1 = "What is the meaning of life"
status2 = "Im tired of the cornavirus "
status3 = "If there is no flour eat cakes"
status4 = "Have a nice week"
status5 = "Im at the beach"
status6 = "Today, barbecue in the woods"
status7 = "Please help us www.cancer.com/Xf58b22"
status8 = "In New York city"
status9 = "There was a crazy workout today"
status10 = "Help us find Max www.myDog.com/Pi10g71"
status11 = "The best burger www.BK.com/Mn47l84"
status12 = "NEWS www.Znet.com/Vj11w05"
status13 = "My cooking photo:)"
status14 = "Amazing song www.AC_DC.com/Yb12a24"
status15 = "I bought an apartment in Tel Aviv"
status16 = "Selling my guitar"
status17 = "The food industry is destroying the world"
status18 = "Meat is murder www.vegetables.com/Vg99j47"
status19 = "Here in Vegas"
status20 = "I lost weight :)"
status21 = "What is change ?!"
status22 = "Wanted waiter for www.MCdonalds.com/Kl46d12"
status23 = "Happy birthday to Liel 25!"
status24 = "Watching Game of Thrones tonight"
status25 = "Save the date www.married1/1/20.com/Uw00u51"
status26 = "Nail polish for $ 10"
status27 = "Look! a new haircut"
status28 = "funny vines www.youtube.com/Fu11y75"
status29 = "I hate emojis"

all_status = [
(status, status),
(status1, status1),
(status2, status2),
(status3, status3),
(status4, status4),
(status5, status5),
(status6, status6),
(status7, status7),
(status8, status8),
(status9, status9),
(status10, status10),
(status11, status11),
(status12, status12),
(status13, status13),
(status14, status14),
(status15, status15),
(status16, status16),
(status17, status17),
(status18, status18),
(status19, status19),
(status20, status20),
(status21, status21),
(status22, status22),
(status23, status23),
(status24, status24),
(status25, status25),
(status26, status26),
(status27, status27),
(status28, status28),
(status29, status29)
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


    PrivacyLoss = '0.1$'
    PrivacyLoss1 = '0.2$'
    PrivacyLoss2 = '0.3$'
    PrivacyLoss2 = '0.4$'
    PrivacyLoss2 = '0.5$'
    PrivacyLoss2 = '0.6$'
    PrivacyLoss2 = '0.7$'
    PrivacyLoss2 = '0.8$'
    PrivacyLoss2 = '0.9$'


    all_PrivacyLoss = [
        (PrivacyLoss, '0.1$'),
        (PrivacyLoss1, '0.2$'),
        (PrivacyLoss2, '0.3$'),
        (PrivacyLoss2, '0.4$'),
        (PrivacyLoss2, '0.5$'),
        (PrivacyLoss2, '0.6$'),
        (PrivacyLoss2, '0.7$'),
        (PrivacyLoss2, '0.8$'),
        (PrivacyLoss2, '0.9$'),


    ]
    PrivacyLoss = models.CharField(
        max_length=50,
        choices=all_PrivacyLoss,
        default='0$',
    )

    burden = '0.1$'
    burden1 = '0.2$'
    burden2 = '0.3$'
    burden3 = '0.4$'
    burden4 = '0.5$'
    burden5 = '0.6$'
    burden6 = '0.7$'
    burden7 = '0.8$'
    burden8 = '0.9$'
    
    all_burden = [
       (burden, '0.1$'),
        (burden1, '0.2$'),
        (burden2, '0.3$'),
        (burden3, '0.4$'),
        (burden4, '0.5$'),
        (burden5, '0.6$'),
        (burden6, '0.7$'),
        (burden7, '0.8$'),
        (burden8, '0.9$'),

    ]
    burden = models.CharField(
        max_length=50,
        choices=all_burden,
        default='0$',
    )


    benefit = '0.1$'
    benefit1 = '0.2$'
    benefit2 = '0.3$'
    benefit3 = '0.4$'
    benefit4 = '0.5$'
    benefit5 = '0.6$'
    benefit6 = '0.7$'
    benefit7 = '0.8$'
    benefit8 = '0.9$'
    
    all_benefit = [
       (benefit, '0.1$'),
        (benefit1, '0.2$'),
        (benefit2, '0.3$'),
        (benefit3, '0.4$'),
        (benefit4, '0.5$'),
        (benefit5, '0.6$'),
        (benefit6, '0.7$'),
        (benefit7, '0.8$'),
        (benefit8, '0.9$'),

    ]
    benefit = models.CharField(
        max_length=50,
        choices=all_benefit,
        default='0$',
    )

    sumWithOutBenefit = models.FloatField(default=0)

    def __str__(self):
        return self.status

class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    date_posted = models.TimeField(default=timezone.now)
    likes = models.ManyToManyField(User,related_name='likes',blank=True)
    
    def __str__(self):
        return str(self.status)
    
    def total_likes(self):
        return self.likes.count()



class Round(models.Model):
    round_number = models.IntegerField(default=0)
    posts_id = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True),size=8,),size=8,)
    likes_id = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True),size=8,),size=8,)

class Ready(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return str(self.user) + ': ' + str(self.date)


class WorkersInfo(models.Model):
    worker_id = models.CharField(max_length=100)
    id_user = models.IntegerField(User,default=0)
    subCode = models.CharField(max_length=100,default="None")


    def __str__(self):
        return str(self.worker_id) + ': ' + str(self.free_comments)

class Log(models.Model):
    id_user = models.IntegerField(User)
    id_round = models.IntegerField(default=0)
    code_operation = models.CharField(max_length=10)
    post_id = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id_round) + ': ' + str(self.id_user) + ': ' + str(self.code_operation)+ ': ' + str(self.post_id)

class ScorePerRound(models.Model):
    id_user = models.IntegerField(User)
    id_round = models.IntegerField(default=0)
    score = models.FloatField(default=0)

    def __str__(self):
        return str(self.id_round) + ': ' + str(self.id_user) + ': ' + str(self.score)



class Score(models.Model):
    id_user = models.IntegerField(User)
    burden = models.FloatField(default=0)
    benefit = models.FloatField(default=0)
    privacy_loss = models.FloatField(default=0)
    final_score = models.FloatField(default=0)

    def __str__(self):
        return str(self.id_user) + ': ' + str(self.burden) + ': ' + str(self.benefit)+ ': ' + str(self.privacy_loss)+ ': ' + str(self.final_score)

class FeedPerUser(models.Model):
    id_user = models.IntegerField(User)
    feedPosts = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True),size=100,),size=100,)

    def __str__(self):
        return str(self.id_user) + ': ' + str(self.feedPosts)

class benefitRounds2(models.Model):
    id_user = models.IntegerField(User)
    round_1 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_2 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_3 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_4 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_5 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_6 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_7 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_8 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_9 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_10 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_11 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_12 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_13 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_14 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_15 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_16 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_17 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_18 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_19 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)
    round_20 = ArrayField(ArrayField(models.IntegerField(unique=True,blank=True,default=None),size=100,default=None),size=100,default=None)

    def __str__(self):
        return str(self.id_user)


class inEndScreen(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)