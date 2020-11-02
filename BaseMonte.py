import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import *
from users.models import AllLogin,Users_free
from facebook.models import Post
from django.contrib.auth.models import User
from properties import *
import facebook.algoritem as algo
from queue import Queue
import copy
import random
import itertools
from timeit import default_timer as timer
import RandomActions as RA
from properties import AF_COST,OF_COST,UL_COST,SL_COST

DeepSize = 5

proOperator = {
    "P" :  0.40,
    "AF" : 0.50,
    "OF" : 0.30,
    "N" :  0.20,
    "SL" : 0.10,
    "UL" : 0.90,
    }


class Node: 

    def __init__(self):
        self.data = []
        self.SimulateScore = 0
        self.SimulatePath = ""
        self.TrueScore = 0
        self.countParents = 0
        self.parent = None
        self.operator = "-1"

    def __str__(self):
        return f'[data: {self.data} ,score: {self.score} ,parent: {self.parent} ,operator: {self.operator}]'


def NodeP(parent,operator,RandomStatusID_1,RandomStatusID_2):
    n1 = Node()
    operatorStr = ""
    n1.parent = parent
    n1.countParents = parent.countParents +1
    if operator[0] == "P" and operator[1] == "P":
        n1.operator = str(parent.operator) + "->" + "[P("+str(RandomStatusID_1)+"),"+"P("+str(RandomStatusID_2)+")]"
        print(n1.operator)
        return n1
    if operator[0] == "P":
        n1.operator = str(parent.operator) + "->" + "[P("+str(RandomStatusID_1)+"),"+str(operator[1])+"]"
        print(n1.operator)
        return n1
    if operator[1] == "P":
        n1.operator = str(parent.operator) + "->" +"["+str(operator[0])+","+"P("+str(RandomStatusID_2)+"]"
        print(n1.operator)
        return n1
    else:
        n1.operator = str(parent.operator) + "->" +"["+str(operator[0])+","+str(operator[1])+"]"
        print(n1.operator)
   
    return n1



def Simulate(UserOperation):
    ValidOperation = ["P","AF","OF","SL","UL"]
    SimulateScore = 0
    SimulatePath = ""
    flag = False
    if UserOperation == "P":
        statusID ,statusValue = getStatusValue()    
        SimulatePath += "P("+str(statusID)+")"
        SimulateScore = statusValue
    else:
        SimulateScore = getValuePerMove(UserOperation)
        SimulatePath = UserOperation

    for i in range(0,DeepSize):
        random.shuffle(ValidOperation)
        random_num = random.uniform(0,1)
        random_num = float('{0:.1f}'.format(random.uniform(0,1)))
        if flag:
            SimulatePath += " ~> "+ "N"
            continue
        flag = True
        for j in ValidOperation:
            flag = True
            if random_num <= proOperator.get(j) and flag :
                flag = False
                print("i = ",i," random_num = ",random_num,j,"pro = ",proOperator.get(j))
                if j == "P":
                    statusID ,statusValue = getStatusValue()
                    SimulateScore += statusValue
                    SimulatePath += " ~> P("+ str(statusID)+")"
                else:
                    SimulateScore += getValuePerMove(j)
                    SimulatePath += " ~> "+ j
                break


    print("Path = "+SimulatePath)
    print("SimulateScore = ",SimulateScore)


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
        return getStatusValue()
    elif move == "N":
        return 0 


def getChlids(po):
    anslist = []
    mylist = []
    for o in po:
        l = []
        for key,value in o.items():
            l.append(key)
        mylist.append(l)

    for element in itertools.product(*mylist):
        anslist.append(element)
    return anslist

def getRandomOpeartion2Players(data):
    random.shuffle(data)
    return data[0][0],data[0][1]


def getStatusValue():
    randomStatusID = RA.getStatusToPostID()
    statusValue = Status.objects.filter(id=randomStatusID).first().sumWithOutBenefit
    return randomStatusID,statusValue


if __name__ == '__main__':
    start = Node()
    Agent_id = 2
    User3_id = 3

    AgentPosts = algo.Post_on_feed(Agent_id)
    User3Posts = algo.Post_on_feed(User3_id)

    AgentOperators = RA.Get_Possible_Operators(Agent_id,AgentPosts)
    User3Opeators = RA.Get_Possible_Operators(User3_id,User3Posts)

    print("AgentOperators = ",AgentOperators)
    print("User3Opeators = ", User3Opeators)
    start.data.append(AgentOperators)
    start.data.append(User3Opeators)
    operators = getChlids(start.data)
    ans = []
    j = 0
    RandomStatusID_1 = RA.getStatusToPostID()
    RandomStatusID_2 = RA.getStatusToPostID()
    for i in operators:
        l = list(operators[j])
        ans.append(NodeP(start,l,RandomStatusID_1,RandomStatusID_2))
        Simulate(l[0])
        j+=1

    AgentMove,User3Move = getRandomOpeartion2Players(getChlids(start.data))
    print("agentMove = ",AgentMove, "User3Move = ",User3Move)
    move1,value1 = RA.MakeMove(Agent_id,AgentMove,AgentOperators)
    move2,value2 = RA.MakeMove(User3_id,User3Move,User3Opeators)
