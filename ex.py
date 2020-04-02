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
friend_my_know = []
for c_user in users:
    if c_user.pk not in friends_requst:
        if c_user.pk not in friends:
            if c_user.pk != 2:
                friend_my_know.append(c_user.pk)

print(friends_requst)
print(friend_my_know)

# user_requsted = User.objects.get(id=4)
# print(f"user_requsted = {user_requsted}")