# import os
# import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
# django.setup()
# from facebook.models import *
# from users.models import AllLogin,Users_free
# from facebook.models import *
# from facebook.views import *
# from django.contrib.auth.models import User
import threading 
import math
# from facebook.views import log
# import facebook.algoritem as algo
from properties import *
import random
from timeit import default_timer as timer
import time
import itertools
# import RandomActions as RA
from queue import Queue
import xlwt 
from xlwt import Workbook 



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


Agnet_SL = 0
User3_SL = 0
Agnet_UL = 0
User3_UL = 0
def MakeMove(userID,move,operatorsAgent,operatorsUser3):
    global Agnet_SL,User3_SL,Agnet_UL,User3_UL
    AgnetOP = operatorsAgent.copy()
    User3OP = operatorsUser3.copy()
    if move == "OF":
        if userID == 2:
            if AgnetOP.get("OF"):
                if User3OP.get("OF"):
                    User3OP.pop("OF")
                AgnetOP.pop("OF")
                User3OP.update({"AF" : 1})

        if userID == 3:
            if User3OP.get("OF"):
                if AgnetOP.get("OF"):
                    AgnetOP.pop("OF")
                User3OP.pop("OF")
                AgnetOP.update({"AF" : 1})

        if AgnetOP.get("AF") and User3OP.get("AF"):
            User3OP.pop("AF")
            AgnetOP.pop("AF")

    elif move == "AF":
        if userID == 2:
            AgnetOP.pop("AF")
            if AgnetOP.get("OF"):
                AgnetOP.pop("OF")
 

        if userID == 3:
            User3OP.pop("AF")
            if User3OP.get("OF"):
                User3OP.pop("OF")

    elif move == "SL":
        if userID == 2:
            User3_SL-= 1
            if User3_SL == 0:
                AgnetOP.pop("SL")
            else:
                AgnetOP.update({"SL" : User3_SL})
        else:
            Agnet_SL-= 1
            if Agnet_SL == 0:
                User3OP.pop("SL")
            else:
                User3OP.update({"SL" : Agnet_SL})          
                

    elif move == "UL":
        if userID == 2:
            User3_UL-= 1
            if User3_UL == 0:
                AgnetOP.pop("UL")
            else:
                AgnetOP.update({"UL" : User3_UL})
        else:
            Agnet_UL-= 1
            if Agnet_UL == 0:
                User3OP.pop("UL")
            else:
                User3OP.update({"UL" : Agnet_UL})   

    elif move == "P":
        toDo = ToPost()
        if userID == 2:
            if toDo == "SL":
                Agnet_SL+=1
                if not User3OP.get("SL"):
                    User3OP.update({"SL" : Agnet_SL})
            else:
                Agnet_UL+=1
                if not User3OP.get("UL"):
                    User3OP.update({"UL" : Agnet_UL})

        else:
            if toDo == "SL":
                User3_SL+=1
                if not User3OP.get("SL"):
                    AgnetOP.update({"SL" : User3_SL})
            else:
                User3_UL+=1
                if not User3OP.get("UL"):
                    AgnetOP.update({"UL" : User3_UL})           

    elif move == "N":
        pass
    return AgnetOP,User3OP


def ToPost():
    if random.randint(0,1) == 0: #  SL
        return "SL"
    else:
        return "UL"


class Node: 

    def __init__(self):
        self.data = []
        self.parent_SL = 0
        self.parent_UL = 0
        self.AgentMove = ""
        self.User3Move = ""
        self.countParents = 0
        self.parent = None
        self.operator = "-1"

    def __str__(self):
        return f'[data: {self.data} ,score: {self.score} ,parent: {self.parent} ,operator: {self.operator}]'


def NodeP(parent,operator):
    n1 = Node()
    n1.parent = parent
    n1.data = parent.data
    n1.AgentMove = operator[0]
    n1.User3Move = operator[1]
    n1.countParents = parent.countParents + 1
    if operator[0] == "P" and operator[1] == "P":
        n1.operator = str(parent.operator) + "->" + "[P,P]"
        # print(n1.operator)
        return n1
    
    if operator[0] == "P":
        n1.operator = str(parent.operator) + "->" + "[P,"+str(operator[1])+"]"
        # print(n1.operator)
        return n1

    if operator[1] == "P":
        n1.operator = str(parent.operator) + "->" +"["+str(operator[0])+","+"P]"
        # print(n1.operator)
        return n1
    else:
        n1.operator = str(parent.operator) + "->" +"["+str(operator[0])+","+str(operator[1])+"]"
        # print(n1.operator)
        return n1
    
def getRandomOpeartion2Players(data):
    random.shuffle(data)
    return data[0][0],data[0][1]


def ExportToExel(TimeAndNodesPerLevel,title):
    wb = Workbook() 
    
    # add_sheet is used to create sheet. 
    sheet1 = wb.add_sheet(title) 
    sheet1.write(0, 0, 'Level') 
    sheet1.write(0, 1, 'Time(sec)') 
    sheet1.write(0, 2, 'Num of nodes') 
    for i in range(0,16):
        sheet1.write(i+1, 0, i) # Level
        sheet1.write(i+1, 1, TimeAndNodesPerLevel[i][0]) # Time 
        sheet1.write(i+1, 2, TimeAndNodesPerLevel[i][1]) # Num of node

    wb.save(title) 


def BFS(start,title):
    timerPerLevel = {}
    for i in range(0,16):
        timerPerLevel.update({i: [0,0]})
    A_move = {}
    U_move = {}
    UF_move = {}
    FA_move = {}
    count = 0
    startr = timer()
    Q = Queue()
    Q.put(start)
    i = 0
    temoCountParent = 0
    startRound = timer()
    while(not Q.empty()):
        node = Q.get()
        if i != 0:
            # print("Agent Move = ",node.AgentMove, "User3 Move =",node.User3Move)
            if node.AgentMove == "OF" and node.User3Move == "OF":
                FA_move = node.data[0].copy()
                UF_move = node.data[1].copy()
                FA_move.pop("OF")
                UF_move.pop("OF")
            else:
                A_move,U_move = MakeMove(2,node.AgentMove,node.data[0],node.data[1])
                FA_move, UF_move = MakeMove(3,node.User3Move,A_move, U_move)
            node.data = []
            node.data.append(FA_move)
            node.data.append(UF_move)
        validOperator = getChlids(node.data)
        # n = 5
        if node.countParents > 8: # untill level  n-1 include!
            print(node.operator)
            endRound = timer()
            timerPerLevel[temoCountParent][0] = (endRound-startRound)
            timerPerLevel[temoCountParent][1] = count
            print("node.countParents = ",node.countParents, "and temoCountParent = ",temoCountParent)
            print("time is ",(endRound-startRound))
            print("total chlids = ",count)
            break
        if node.countParents == temoCountParent+1:
            endRound = timer()
            print("node.countParents = ",node.countParents, "and temoCountParent = ",temoCountParent)
            print("time is ",(endRound-startRound))
            print("total chlids = ",count)
            timerPerLevel[temoCountParent][0] = (endRound-startRound)
            timerPerLevel[temoCountParent][1] = count
            print((endRound-startRound))
            temoCountParent+=1
            startRound = timer()
            ExportToExel(timerPerLevel,title)


        j = 0
        for o in validOperator:
            l = list(validOperator[j])
            n = NodeP(node,l)
            Q.put(n)
            count+=1
            j+=1
        i+=1

    end = timer()
    print((end-startr))
    print("total chlids = ",count)
    print("TimePerLevel",timerPerLevel)
    ExportToExel(timerPerLevel,title)
    sumit = 0
    for key,value in timerPerLevel.items():
        
        sumit+=value[0]
    print("total time= ",sumit)

if __name__ == '__main__':
    # data = []
    AgentOperators = {'OF': 1, 'P': 'Posts', 'N': 'None'}
    User3Operators = {'OF': 1, 'P': 'Posts', 'N': 'None'}
    start = Node()

    start.data.append(AgentOperators)
    start.data.append(User3Operators)

    BFS(start,"64vCPU - 416GB Memory Test.xls")

