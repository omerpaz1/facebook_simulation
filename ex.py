import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import Post,Status,Friends,Friend_req
from django.contrib.auth.models import User




    # context = {
    #     'posts' : Post.objects.order_by('-date_posted'),
    #     'mystatus' : Status.objects.all(),
    #     'friends' : Friends.objects.filter(userid_id=request.user.id).first().myfriends,
    #     'friends_requst' : list(set(Friend_req.objects.filter(userid_id=request.user.id).first().myfriends_req)),
    #     'users' : User.objects.all()
    # }
friends = Friends.objects.filter(userid_id=1).first().myfriends
friends_requst = list(set(Friend_req.objects.filter(userid_id=1).first().myfriends_req))
users = User.objects.all()


current_user_table = Friend_req.objects.filter(userid_id=5).first()
# x = len(current_user_table.myfriends_req)
# for _ in range(1,x):
#     if current_user_table.myfriends_req[_] == 1:
#         print(_)
to_delete = []
for friendid in current_user_table.myfriends_req:
    if friendid == 1:
        to_delete.append(friendid)