import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_simulation.settings')
django.setup()
from facebook.models import *
from users.models import AllLogin,Users_free
from facebook.models import Post
from django.contrib.auth.models import User
import threading 
import math
from facebook.views import posts_user_liked
import facebook.algoritem as algo
from properties import *
import random
from timeit import default_timer as timer
import time
from queue import Queue
import copy
import threading 



validOperator = ["P","OF","AF","N"]



class Node: 

    def __init__(self):
        self.score = 0
        self.countParents = 0
        self.parent = None
        self.operator = "-1"
        self.currentPosts = getAllStatus()


            

    def __str__(self):
        return f'[score: {self.score} ,parent: {self.parent} ,operator: {self.operator}]'

def NodeP(parent,operator):
    n1 = Node()
    if operator == "P":
        n1.currentPosts = copy.deepcopy(parent.currentPosts)
        p = next(iter(n1.currentPosts))
        n1.score =  parent.score + n1.currentPosts.get(p)
        n1.parent = parent
        n1.countParents = parent.countParents +1
        n1.operator = str(parent.operator)+ "->P("+str(p)+")"
        n1.currentPosts.pop(p)
        print(n1.operator)
        return n1
    else:
        n1.currentPosts = copy.deepcopy(parent.currentPosts)
        n1.score = parent.score + getValuesOperations().get(operator)
        n1.parent = parent    
        n1.countParents = parent.countParents + 1
        n1.operator = str(parent.operator) + "->" + str(operator)
        print(n1.operator)
        return n1



def getValuesOperations():
    operations = {}

    operations.update({'OF' : OF_COST})
    operations.update({'AF' : AF_COST})
    operations.update({'SL' : SL_COST})
    operations.update({'UL' : UL_COST})
    operations.update({'P' : algo.getAllStatus()})
    operations.update({'N' : 0})
    return operations

def getInfo(node):
    print("Max Score = ",node.score)

def getAllStatus():
    a = Status.objects.all()
    posts = {}
    for i in a:
        posts.update({i.id : i.sumWithOutBenefit})

    all_status = {}

    for i in range(30):
        key = max(posts,key=posts.get)
        value = posts.get(key)
        posts.pop(key)
        all_status.update({key : value})

    return all_status

def BFS():
    count = 0
    startr = timer()
    start = Node()
    s = []
    MaxNode = start
    Q = Queue()
    Q.put(start)
    s.append(start)
    while(not Q.empty()):
        node = Q.get()
        if node.score >= MaxNode.score:
            MaxNode = node
        if node.countParents > 15:
            print(node.operator)
            break
        for o in validOperator:
            n = NodeP(node,o)
            Q.put(n)
            count+=1
        print("total chlids = ",count)
    end = timer()
    print((end-startr)/60)
    print(count)



if __name__ == '__main__':

    BFS()

    

