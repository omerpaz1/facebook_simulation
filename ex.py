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
# friends = Friends.objects.filter(userid_id=1).first().myfriends
# friends_requst = list(set(Friend_req.objects.filter(userid_id=1).first().myfriends_req))
# users = User.objects.all()
# u = []
# posts = Post.objects.all()
# for post in posts:
#     u.append(post.likes.filter(id=1).values_list('post', flat=True).first())

# print(u)

posts = Post.objects.all()
u = []
for p in posts:
    if p.likes.filter(id=1).values_list('likes', flat=True).first() is not None:
        post_i_liked = p.likes.filter(id=1).values_list('likes', flat=True).first()
        u.append(post_i_liked)

for post in posts:
    if post.id in u:
        print(post.id)