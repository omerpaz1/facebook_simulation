from .models import *


# this function will return to each user heis posts lists.
def Post_on_feed(user_id):  
    add_posts_to_current_round()



def add_posts_to_current_round():
    all_posts = Post.objects.all()
    rounds = Round.objects.all()
    print(rounds)

