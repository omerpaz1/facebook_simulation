from django.shortcuts import render

posts = [
    {
        'username': 'userA',
        'status': 'its a nice day!',
        'date_posted' : '19/3/2020'
    },
    {
        'username': 'userB',
        'status': 'I like Pizza',
        'date_posted': '17/3/2020'
    }
]
# comments = [
#     {
#         "postid" : '1',
#         "username" : 'userB',
#         "comment1": 'i like pizza',
#         'date_comment': '19/3/2020'
#     }
# ]




def home(request):
    context = {
        'posts' : posts
    }
    return render(request,'facebook/post.html',context)


def create_first_post(request):
    return render(request,'facebook/create_first_post.html',{'title': 'create post'})