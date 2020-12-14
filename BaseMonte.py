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
    "P" :  0.70,
    "AF" : 0.60,
    "OF" : 0.20,
    "N" :  0.30,
    "SL" : 0.40,
    "UL" : 0.50,
    }


class Node: 

    def __init__(self):
        self.data = []
        self.SimulateScore = 0
        self.SimulatePath = ""
        self.TrueScoreAgent = 0
        self.TrueScoreUser3 = 0
        self.AgnetOperator = "P"
        self.User3Operator = "P"
        self.operatorValue = ""
        self.countParents = 0
        self.parent = None
        self.operator = "-1"

    def __str__(self):
        return f'[data: {self.data} ,score: {self.score} ,parent: {self.parent} ,operator: {self.operator}]'


def NodeP(parent,operator,RandomStatusID_1,RandomStatusID_2):
    n1 = Node()
    operatorStr = ""
    n1.parent = parent
    n1.countParents = parent.countParents + 1
    if operator[0] == "P" and operator[1] == "P":
        n1.operator = str(parent.operator) + "->" + "[P("+str(RandomStatusID_1)+"),"+"P("+str(RandomStatusID_2)+")]"
        n1.TrueScoreAgent += parent.TrueScoreAgent + getStatusValue(RandomStatusID_1)
        n1.TrueScoreUser3 += parent.TrueScoreUser3 + getStatusValue(RandomStatusID_2)
        print(n1.operator)
        return n1

    
    if operator[0] == "P":
        n1.operator = str(parent.operator) + "->" + "[P("+str(RandomStatusID_1)+"),"+str(operator[1])+"]"
        n1.TrueScoreAgent += parent.TrueScoreAgent + getStatusValue(RandomStatusID_1)
        n1.TrueScoreUser3 += parent.TrueScoreUser3 + getValuePerMove(operator[1])
        print(n1.operator)
        return n1
    if operator[1] == "P":
        n1.operator = str(parent.operator) + "->" +"["+str(operator[0])+","+"P("+str(RandomStatusID_2)+"]"
        n1.TrueScoreAgent += parent.TrueScoreAgent + getValuePerMove(operator[0])
        n1.TrueScoreUser3 += parent.TrueScoreUser3 + getStatusValue(RandomStatusID_2)
        print(n1.operator)
        return n1
    else:
        n1.operator = str(parent.operator) + "->" +"["+str(operator[0])+","+str(operator[1])+"]"
        n1.TrueScoreAgent += parent.TrueScoreAgent + getValuePerMove(operator[0])
        n1.TrueScoreUser3 += parent.TrueScoreUser3 + getValuePerMove(operator[1])
        print(n1.operator)
        return n1
    return n1


def getRandomOperation():
    ValidOperation = ["P","AF","OF","SL","UL"]
    random.shuffle(ValidOperation)
    random_num = random.uniform(0,1)
    random_num = float('{0:.1f}'.format(random.uniform(0,1)))
    for i in ValidOperation:
        if random_num <= proOperator.get(i):
            return i
    return "N"



def Simulate(UserOperation):
    SimulateScore = 0
    SimulatePath = ""

    for i in range(0,DeepSize):
        j = getRandomOperation()
        if j == "P":
            statusID ,statusValue = getStatus()
            SimulateScore += statusValue
        else:
            SimulateScore += getValuePerMove(j)
    return SimulateScore


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
        return getStatus()
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


def getStatus():
    randomStatusID = RA.getStatusToPostID()
    statusValue = Status.objects.filter(id=randomStatusID).first().sumWithOutBenefit
    return randomStatusID,statusValue

def getStatusValue(statusID):
    return Status.objects.filter(id=statusID).first().sumWithOutBenefit


def MCTS():
    start = Node()
    Agent_id = 2
    User3_id = 3

    AgentPosts = algo.Post_on_feed(Agent_id)
    User3Posts = algo.Post_on_feed(User3_id)

    AgentOperators = RA.Get_Possible_Operators(Agent_id,AgentPosts)
    User3Opeators = RA.Get_Possible_Operators(User3_id,User3Posts)

    start.data.append(AgentOperators)
    start.data.append(User3Opeators)

    myPath = []
    myPath.append(start)
    while True:
        node = myPath.pop()
        if node.countParents > 2:
            print("Final Path = ",node.operator)
            print("TrueScoreAgent = ",node.TrueScoreAgent)
            break
        
        operators = getChlids(node.data)
        j = 0
        SimulateMax = -100
        AgentMaxOperation = ''
        User3RanOperation = ''
        MaxNode = node
        RandomStatusID_1 = RA.getStatusToPostID()
        RandomStatusID_2 = RA.getStatusToPostID()
        for i in operators:
            l = list(operators[j])
            n = NodeP(node,l,RandomStatusID_1,RandomStatusID_2)
            SimulateScore = Simulate(l[0])
            n.SimulateScore = n.TrueScoreAgent + SimulateScore
            if n.SimulateScore > SimulateMax:
                MaxNode = n                
                SimulateMax = n.SimulateScore
                AgentMaxOperation = l[0]
                User3RanOperation = l[1]
            j+=1

        myPath.append(MaxNode)


        print(operators)
        print("AgentMaxOperation = ",AgentMaxOperation, "User3RanOperation = ",User3RanOperation)
        move1,value1 = RA.MakeMove(Agent_id,AgentMaxOperation,AgentOperators)
        move2,value2 = RA.MakeMove(User3_id,User3RanOperation,User3Opeators)

        AgentPosts = algo.Post_on_feed(Agent_id)
        User3Posts = algo.Post_on_feed(User3_id)
        AgentOperators = RA.Get_Possible_Operators(Agent_id,AgentPosts)
        User3Opeators = RA.Get_Possible_Operators(User3_id,User3Posts)

        MaxNode.data.append(AgentOperators)
        MaxNode.data.append(User3Opeators)


def BFS():
    start = Node()
    Agent_id = 2
    User3_id = 3

    count = 0
    startr = timer()
    start = Node()
    MaxNode = start
    Q = Queue()
    Q.put(start)
    while(not Q.empty()):
        node = Q.get()
        AgentPosts = algo.Post_on_feed(Agent_id)
        User3Posts = algo.Post_on_feed(User3_id)

        AgentOperators = RA.Get_Possible_Operators(Agent_id,AgentPosts)
        User3Opeators = RA.Get_Possible_Operators(User3_id,User3Posts)

        node.data.append(AgentOperators)
        node.data.append(User3Opeators)

            
        print(node.countParents)
        if node.countParents > 3:
            print(node.operator)
            break


        validOperator = getChlids(node.data)
        j = 0
        RandomStatusID_1 = RA.getStatusToPostID()
        RandomStatusID_2 = RA.getStatusToPostID()
        MaxValueChilds = -100
        for o in validOperator:
            l = list(validOperator[j])
            n = NodeP(node,l,RandomStatusID_1,RandomStatusID_2)

            Q.put(n)
            count+=1
            j+=1
        AgentMaxOperation,User3RanOperation = getRandomOpeartion2Players(validOperator)
        print("AgentMaxOperation = ",AgentMaxOperation, "User3RanOperation = ",User3RanOperation)
        move1,value1 = RA.MakeMove(Agent_id,AgentMaxOperation,AgentOperators)
        move2,value2 = RA.MakeMove(User3_id,User3RanOperation,User3Opeators)
        print("total chlids = ",count)
    end = timer()
    print((end-startr)/60)
    print(count)


if __name__ == '__main__':



    agentPosts = algo.Post_on_feed(2)

    AgentOperators = RA.Get_Possible_Operators(2,agentPosts)

    print(list(AgentOperators.keys()))