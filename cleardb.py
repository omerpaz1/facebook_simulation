import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import Post,Status,Friends,Friend_req
from django.contrib.auth.models import User

friends1 = Friends.objects.filter(userid_id=1).first()
friends2 = Friends.objects.filter(userid_id=2).first()
friends3 = Friends.objects.filter(userid_id=3).first()
friends4 = Friends.objects.filter(userid_id=4).first()
friends5 = Friends.objects.filter(userid_id=5).first()

friends1.myfriends.clear()
friends2.myfriends.clear()
friends3.myfriends.clear()
friends4.myfriends.clear()
friends5.myfriends.clear()

friends1.save()
friends2.save()
friends3.save()
friends4.save()
friends5.save()


friends1 = Friend_req.objects.filter(userid_id=1).first()
friends2 = Friend_req.objects.filter(userid_id=2).first()
friends3 = Friend_req.objects.filter(userid_id=3).first()
friends4 = Friend_req.objects.filter(userid_id=4).first()
friends5 = Friend_req.objects.filter(userid_id=5).first()

friends1.myfriends_req.clear()
friends2.myfriends_req.clear()
friends3.myfriends_req.clear()
friends4.myfriends_req.clear()
friends5.myfriends_req.clear()

friends1.save()
friends2.save()
friends3.save()
friends4.save()
friends5.save()