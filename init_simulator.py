import os
import sys
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import Post,Status,Friends,Friend_req,Round,Ready,Log,WorkersInfo,Score,inEndScreen,benefitRounds2
from users.models import Profile
from django.contrib.auth.models import User
from users.models import AllLogin,Users_free
from properties import agent_id,adminUser

try:
    flag = sys.argv[2]
    flag = True
except:
    flag = False

users = ['Riley','Jordan','Parker','Harley','Kendall','Quinn']
status = ['I like Pizza',
        'i hate emojis',
	    'What is the meaning of life',
            'Im tired of the cornavirus',
            'If there is no flour eat cakes',
    	    'Have a nice week',
	    'Im at the beach',
	    'Today, barbecue in the woods',
            'Please help us www.cancer.com/Xf58b22',
            'In New York city',
    	    'There was a crazy workout today',
	    'Help us find Max www.myDog.com/Pi10g71',
	    'The best burger www.BK.com/Mn47l84',
            'NEWS www.Znet.com/Vj11w05',
            'My cooking photo:)',
    	    'Amazing song www.AC_DC.com/Yb12a24',
	    'I bought an apartment in Tel Aviv',
	    'Selling my guitar',
            'The food industry is destroying the world',
            'Meat is murder www.vegetables.com/Vg99j47',
    	    'Here in Vegas',
	    'I lost weight :)',
	    'What is "change" ?!',
            'Wanted waiter for www.MCdonalds.com/Kl46d12',
            'Happy birthday to Liel 25!',
    	    'Watching Game of Thrones tonight',
	    'Save the date www.married1/1/20.com/Uw00u51',
	    'Nail polish for $ 10',
            'Look! a new haircut',
            'funny vines www.youtube.com/Fu11y75'
           ]
profile_pic = ['img_A','img_B','img_C','img_D','img_E']
# must do first after change db!
def init_friends():
    allusers = User.objects.all()
    Friends.objects.all().delete()
    for i in users:
        user = allusers.filter(username=i).first()
        f = Friends(userid_id=user.id,myfriends=[])
        f.save()

# must do first after change db!
def init_benefitRounds():
    allusers = User.objects.all()
    benefitRounds2.objects.all().delete()
    for i in users:
        user = allusers.filter(username=i).first()
        f = benefitRounds2(id_user=user.id,round_1=[],round_2=[],round_3=[],round_4=[],round_5=[],round_6=[],round_7=[],round_8=[],round_9=[],round_10=[],round_11=[],round_12=[],round_13=[],round_14=[],round_15=[])
        f.save()

# must do first after change db!
def init_users_score():
    Score.objects.all().delete()
    allusers = User.objects.all()
    for i in allusers:
        if i.id != adminUser:
            user = allusers.filter(username=i).first()
            s = Score(id_user=user.id,burden=0,benefit=0,privacy_loss=0,final_score=0)
            s.save()


def init_friends_requst():
    Friend_req.objects.all().delete()
    allusers = User.objects.all()
    for i in users:
        user1 = allusers.filter(username=i).first()
        f = Friend_req(userid_id=user1.id,myfriends_req=[])
        f.save()

def init_users_free():
    allusers = User.objects.all()
    Users_free.objects.all().delete()
    for i in allusers:
        if i.id != agent_id and i.id != adminUser:
            user = allusers.filter(username=i).first()
            f = Users_free(user_id=user.id)
            f.save()

def init_status():
    Status.objects.all().delete()
    for i in status:
        s = Status(status=i,has_link=False)
        s.save()


def delete_workers_alocate():
    allusers = User.objects.all()
    for i in range(3,len(users)+2):
        user = Users_free.objects.filter(user_id=i).first()
        user.worker_id = "None"
        user.save() 


def delete_friends():
    # friends1 = Friends.objects.filter(userid_id=1).first()
    friends2 = Friends.objects.filter(userid_id=2).first()
    friends3 = Friends.objects.filter(userid_id=3).first()
    friends4 = Friends.objects.filter(userid_id=4).first()
    friends5 = Friends.objects.filter(userid_id=5).first()
    friends6 = Friends.objects.filter(userid_id=6).first()
    friends7 = Friends.objects.filter(userid_id=7).first()

    # friends1.myfriends.clear()
    friends2.myfriends.clear()
    friends3.myfriends.clear()
    friends4.myfriends.clear()
    friends5.myfriends.clear()
    friends6.myfriends.clear()
    friends7.myfriends.clear()

    # friends1.myfriends.append(1) # omerpaz
    friends2.myfriends.append(2)
    friends3.myfriends.append(3)
    friends4.myfriends.append(4)
    friends5.myfriends.append(5)
    friends6.myfriends.append(6)
    friends7.myfriends.append(7)


    # friends1.save()
    friends2.save()
    friends3.save()
    friends4.save()
    friends5.save()
    friends6.save()
    friends7.save()

def delete_friend_req():
    # friends1 = Friend_req.objects.filter(userid_id=1).first()
    friends2 = Friend_req.objects.filter(userid_id=2).first()
    friends3 = Friend_req.objects.filter(userid_id=3).first()
    friends4 = Friend_req.objects.filter(userid_id=4).first()
    friends5 = Friend_req.objects.filter(userid_id=5).first()
    friends6 = Friend_req.objects.filter(userid_id=6).first()
    friends7 = Friend_req.objects.filter(userid_id=7).first()


    # friends1.myfriends_req.clear()
    friends2.myfriends_req.clear()
    friends3.myfriends_req.clear()
    friends4.myfriends_req.clear()
    friends5.myfriends_req.clear()
    friends6.myfriends_req.clear()
    friends7.myfriends_req.clear()

    # friends1.save()
    friends2.save()
    friends3.save()
    friends4.save()
    friends5.save()
    friends6.save()
    friends7.save()

def delete_all_rounds():
    Round.objects.all().delete()

def delete_all_posts():
    Post.objects.all().delete()

def delete_all_likes():
    Post.likes.through.objects.all().delete()

def logout_all():
    AllLogin.objects.all().delete()    

def unReady_all():
    Ready.objects.all().delete()

def delete_operation_info():
    Log.objects.all().delete()

def delete_workers_info():
    WorkersInfo.objects.all().delete()


def delete_inEndScreen():
    inEndScreen.objects.all().delete()



if __name__ == "__main__":
    '''
    use this init only when chagne DB.
    '''
    # init_friends()
    # init_friends_requst()
    # init_status()
    # init_users_free() 
    init_benefitRounds()
    init_users_score()
    '''
    # init DB for next simulation.
    # '''
    delete_all_rounds()
    delete_all_posts()    
    delete_all_likes()
    delete_friend_req()
    delete_friends()
    delete_workers_alocate()
    logout_all()
    unReady_all()   


    # '''
    # only if you dont need anymore the data from the workers and the LOG.

    # '''
    delete_operation_info()
    delete_workers_info()