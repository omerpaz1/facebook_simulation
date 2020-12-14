import os
import django
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.views import *
import time
from django.contrib.auth.models import User
from facebook.models import Post,Status,Friends,Friend_req,Ready
from users.views import *
import requests
from django.contrib.auth.models import AnonymousUser
from django.core.handlers.wsgi import WSGIRequest
from io import StringIO ## for Python 3
from django.urls import resolve
import random
import facebook.algoritem as algo
from timeit import default_timer as timer
from properties import AF_COST,OF_COST,UL_COST,SL_COST
from Util import toExel
from properties import total_rounds
from properties import Users_num
from properties import agent_id
from properties import site_path

# Users_num = 3

# site path 
# site_path = 'http://34.89.133.90/'
PostsIUsed = {}

# DEBUG mode for the prints
DEBUG = True

# Agent info.
userid = agent_id
agent = User.objects.filter(id=userid).first()


probOperator = {
        "P" :  [0.35,0.65],
        "AF" : [0.15,0.35],
        "OF" : [0.65,0.85],
        "N" :  [0.85,1],
        "SL" : [0.05,0.15],
        "UL" : [0.00,0.05],
}

def MyRequest(method='GET',path=site_path, user=agent, params={}):
  """ Construct a fake request(WSGIRequest) object"""
  req = WSGIRequest({
          'REQUEST_METHOD': method,
          'PATH_INFO': path,
          'wsgi.input': StringIO()})

  req.user = user

  req.content_params = params
  return req
AgentRequest = MyRequest(method='POST',path=site_path+'login')


'''
this function will return list of the name of the relevant operations.
param: AR - AgentRequest
the operations: 
1. OF (Offer Friendship)
2. AF (Accept Friendship)
3. SL (Safe like link)
4. UL (UnSafe like link)
4. P (Post)
5. N (None)
'''
def Get_Possible_Operators(userid,current_posts):
    operations = {}

    # 1 -> OF
    PeopleMayKnow = algo.getPeopleMayKnow(userid)
    if PeopleMayKnow: # if there is users not in your friends
        operations.update({'OF' : PeopleMayKnow})

    # 2 -> AF
    FriendRequests = algo.getFriendsRequest(userid)
    if FriendRequests: # if there is users in your friends requests
        operations.update({'AF' : FriendRequests})

    # 3 -> SL
    Optional_SAFE_LikePostsList,Optional_UN_SAFE_LikePostsList = getOptinalLikesPostsAll(userid,current_posts)
    if Optional_SAFE_LikePostsList: # if the there is posts optional to like.
        operations.update({'SL' : Optional_SAFE_LikePostsList})
    if Optional_UN_SAFE_LikePostsList:
        operations.update({'UL' : Optional_UN_SAFE_LikePostsList})

    # 4 -> P
    operations.update({'P' : algo.getAllStatus()})

    # 5 -> N
    operations.update({'N' : 'None'})
    return operations



def getOptinalLikesPostsAll(userid,current_posts):
    currentPostsOnFeed = algo.getIdPosts(current_posts)
    Optional_SAFE_LikePostsList = []
    Optional_UN_SAFE_LikePostsList = []
    for p in currentPostsOnFeed: # about post with no like. same probability.]
        post = Post.objects.filter(id=p).first()
        if post.username_id != userid:
                post_i_liked = post.likes.filter(id=userid).values_list('likes', flat=True).first()
                if post_i_liked != None:
                    continue
                status =  Status.objects.filter(id=post.status_id).first()
                if status.has_link:
                    Optional_UN_SAFE_LikePostsList.append(p)
                else:
                    Optional_SAFE_LikePostsList.append(p)
    return Optional_SAFE_LikePostsList,Optional_UN_SAFE_LikePostsList



def GoToSuccessor(move):
    current_path = site_path
    if move == "OF":
        AgentRequest = MyRequest(method='GET',path=site_path+'home')
        userIdToAdd = getFriendToAdd(Possible_Operators[move])
        userObj = User.objects.filter(id=userIdToAdd).first()
        addfriend(AgentRequest,userObj)
        return "OF", userIdToAdd

    elif move == "AF":
        AgentRequest = MyRequest(method='GET',path=site_path+'home')
        userToConfirm = getFriendToConfirm(Possible_Operators[move])
        userObj = User.objects.filter(id=userToConfirm).first()
        confirm_friends(AgentRequest,userObj)
        return "AF", userToConfirm

    elif move == "SL":
        PostToLike = getPostToLike(Possible_Operators[move])
        AgentRequest = MyRequest(method='POST',path=site_path+'home',params={'post_id': PostToLike})
        like_post_Agent(AgentRequest,"SL")
        return "SL", PostToLike

    elif move == "UL":
        PostToLike = getPostToLike(Possible_Operators[move])
        AgentRequest = MyRequest(method='POST',path=site_path+'home',params={'post_id': PostToLike})
        like_post_Agent(AgentRequest,"UL")
        return "UL", PostToLike

    elif move == "N":
        log(agent.id,"N")
        return "N", "None"

def GoToSuccessorPost(statusID):
        StatusToPost = getStatusToPost(statusID)
        AgentRequest = MyRequest(method='POST',path=current_path+'home' ,params={'user_option_on_feed': StatusToPost})
        home_Agent(AgentRequest)
        return "P", StatusToPost


class Node: 

    def __init__(self):
        self.data = []
        self.SimulateScore = 0
        self.PostID = 0
        self.TrueScoreAgent = 0
        self.AgnetOperator = "P"
        self.countParents = 0
        self.parent = None
        self.operator = "-1"

    def __str__(self):
        return f'[data: {self.data} ,score: {self.score} ,parent: {self.parent} ,operator: {self.operator}]'


'''
this function will return status from all the status in unfomly way.
'''
def getStatusToPost(statusID):
    status = Status.objects.filter(id=statusID).first().status
    PostsIUsed.pop(statusID)
    return status

'''
this function will return from the optional 'people you may know' list one user id in unifomly way
'''
def getFriendToAdd(PeopleMayKnowList):
    random_num = random.randint(0,len(PeopleMayKnowList)-1) # unifom random in all the status.
    return PeopleMayKnowList[random_num]

'''
this function will return post that optinal to like in unimofly way.
'''
def getPostToLike(OptionalPostsToLike):
    random_num = random.randint(0,len(OptionalPostsToLike)-1) # unifom random in all the status.
    return OptionalPostsToLike[random_num]

'''
this function will return post that optinal to friend to confirm in unimofly way.
'''
def getFriendToConfirm(FriendRequests):
    random_num = random.randint(0,len(FriendRequests)-1) # unifom random in all the status.
    return FriendRequests[random_num]

def getValuePerMove(move):
    if move == "OF":
        return OF_COST
    elif move == "AF":
        return AF_COST
    elif move == "SL":
        return SL_COST
    elif move == "UL":
        return UL_COST
    elif move == "P":
        key = max(PostsIUsed,key=PostsIUsed.get)
        value = PostsIUsed.get(key)
        return key,value
    elif move == "N":
        return 0 

def getRandomOperation(ValidOperation):
    # ValidOperation = ["P","AF","OF","SL","UL","N"]
    random_num = random.uniform(0,1)
    random_num = float('{0:.2f}'.format(random.uniform(0,1)))
    for i in ValidOperation:
        if random_num >= probOperator.get(i)[0] and random_num <= probOperator.get(i)[1]:
            return i
    return "N"

postUse = []

def Simulate(UserOperation,operators,num_round):
    SimulateScore = 0
    SimulatePath = ""
    DeepSize = 5
    postUse = []
    diff = total_rounds - num_round 
    if diff < 5:
        DeepSize = diff
    for i in range(0,DeepSize):
        j = getRandomOperation(operators)
        if j == "P":
            key,value = getStatusNotUsed(postUse)
            postUse.append(key)
            SimulateScore += value
            SimulatePath += "~> P("+str(key)+")"
        else:
            SimulateScore += getValuePerMove(j)
            SimulatePath += "~>"+j+""
    print("Simulate =",SimulatePath)
    print("Score of the Simulate =",SimulateScore)
    return SimulateScore

def NodeP(parent,operator):
    n1 = Node()
    n1.parent = parent
    n1.countParents = parent.countParents + 1
    if operator == "P":
        key = max(PostsIUsed,key=PostsIUsed.get)
        statusID = Status.objects.filter(id=key).first().status
        n1.PostID = statusID
        n1.operator = str(parent.operator) + "->" + "[P("+str(statusID)+")]"
        n1.TrueScoreAgent += parent.TrueScoreAgent + PostsIUsed.get(key)
        print(n1.operator)
        return n1
    else:
        value = getValuePerMove(operator)
        n1.operator = str(parent.operator) + "->" + "[("+str(operator)+")]"
        n1.TrueScoreAgent += parent.TrueScoreAgent + value
        print(n1.operator)
        return n1
    return n1

def getStatusNotUsed(iUsed):
    myp = PostsIUsed.copy()
    sot = sorted(myp,key=myp.get,reverse=True)
    for key in sot:
        if key not in iUsed:
            return key,myp.get(key)
    return -1
        

# -----------------------------------------Start Simulation -----------------------------------

# # Log in into the Web Page
if(DEBUG):
    print("Try to login to site")

try:
    login_logger(AgentRequest,AgentRequest,AgentRequest.user)
except:
    print('problem with log in')

if(DEBUG):
    print("Login successful to site")


#  waiting to start simulation
if(DEBUG):
    print("Waiting in the Wait page")
users_login = AllLogin.objects.all()
while(len(users_login) < Users_num):
    users_login = AllLogin.objects.all()
    time.sleep(2)

if(DEBUG):
    print("move from the waiting room to Create Post Page")


''' 
in the Create Post page.
'''

status = Status.objects.all()
for i in status:
    PostsIUsed.update({i.id : i.sumWithOutBenefit})

allStatusValues = {}
status = Status.objects.all()
for i in status:
    allStatusValues.update({i.id : i.sumWithOutBenefit})

if(DEBUG):
    print("Create Post in Create post page")


# Create The First Round!
current_posts = algo.Post_on_feed(agent.id)
time.sleep(2)
current_path = site_path+'create_post'

timePerRound = []
AgentTimeStart = timer()
key = max(PostsIUsed,key=PostsIUsed.get)
StatusToPost = getStatusToPost(key)
AgentRequest = MyRequest(method='POST',path=current_path ,params={'user_option': StatusToPost})
create_post_Agent(AgentRequest)
AgentTimeEnd = timer()
AgentTimeTook = (AgentTimeEnd-AgentTimeStart)/60
mylog = Log.objects.filter(id_user=agent_id).last()
mylog.TimeTookInSec = AgentTimeTook
mylog.save()


# Add to Timer

if(DEBUG):
    print("Join to the ready room for the first time.")

''' 
Send For the First time the Agent to the Ready Room
'''
current_path = site_path+'ready'
AgentRequest = MyRequest(method='GET',path=current_path)

start = Node()
First_Possible_Operators = Get_Possible_Operators(userid,current_posts)
users_ready = set(Ready.objects.values_list('user_id', flat=True))
num_round = 1
start.data.append(First_Possible_Operators)
myPath = []
myPath.append(start)
start.operator += str(start.operator) + "->" + "[P("+str(StatusToPost)+")]"


while(num_round != total_rounds):
    while(len(users_ready) != Users_num):        
        users_ready = set(Ready.objects.values_list('user_id', flat=True))
        if agent_id not in users_ready and len(users_ready) != Users_num:
            print("Join to Ready")
            Ready.objects.create(user=AgentRequest.user) #create new Ready User
    print("Out of ready, Make Move!")
    current_posts = algo.Post_on_feed(agent.id)
    time.sleep(2)
    Ready.objects.all().delete()    
    readyList = []
    '''
    Do Here Algoritem and And Send a Request to the operation.
    '''
    
    Possible_Operators = Get_Possible_Operators(userid,current_posts)
    print("Possible_Operators For The Current Round:\n")
    print(Possible_Operators)
    print('\n')
    
    users_ready = set(Ready.objects.values_list('user_id', flat=True))
    num_round+=1
    startRound = timer()
    print(f"num round = {num_round}")
    while(len(users_ready) < Users_num-1):
        users_ready = set(Ready.objects.values_list('user_id', flat=True))
    endRound = timer()
    tookTime = (endRound-startRound)/60
    print(f"Round Number {num_round}, took: {tookTime} Minutes")
    # Add to Timer

    # Implments MCTS
    AgentTimeStart = timer()
    operators = list(Possible_Operators.keys())
    j = 0
    SimulateMax = -100
    AgentMaxOperation = ''
    node = myPath.pop()
    MaxNode = node
    for i in operators:
        n = NodeP(node,i)
        SimulateScore = Simulate(i,operators,num_round)
        n.SimulateScore = n.TrueScoreAgent + SimulateScore
        if n.SimulateScore > SimulateMax:
            MaxNode = n              
            SimulateMax = n.SimulateScore
            AgentMaxOperation = i
        j+=1

    myPath.append(MaxNode)

    print(operators)
    print("AgentMaxOperation = ",AgentMaxOperation)
    if AgentMaxOperation == "P":
        statusID,val = getValuePerMove("P") # return the value + the current value state
        move,value = GoToSuccessorPost(statusID)
       
    else:
        move,value = GoToSuccessor(AgentMaxOperation)

    AgentTimeEnd = timer()
    AgentTimeTook = (AgentTimeEnd-AgentTimeStart)/60
    print(f"(Agent) Round Number {num_round}, took: {AgentTimeTook} Minutes")
    mylog = Log.objects.filter(id_user=agent_id).last()
    mylog.TimeTookInSec = AgentTimeTook
    mylog.save()
    # End MCTS


    print(f'MakeMove Pick: Operator = {move} , value = {value}\n')

    users_ready = set(Ready.objects.values_list('user_id', flat=True))
    print('----------------  # End Round----------------\n')

Ready.objects.create(user=AgentRequest.user) #create new Ready User
users_ready = set(Ready.objects.values_list('user_id', flat=True))

while(len(users_ready) != Users_num):        
        users_ready = set(Ready.objects.values_list('user_id', flat=True))

time.sleep(5)
Ready.objects.all().delete()    
readyList = []

algo.UpdateScoreStatic(userid)
node = myPath.pop()
print("MaxNode Path = ",node.operator)
print("Score Agent = ",node.TrueScoreAgent)
print("Simulrator Finished")