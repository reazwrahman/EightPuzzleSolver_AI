#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 19:53:29 2021

@author: Reaz
"""


import sys
import math
import time
import queue as Q

## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)  
        
        ## declare the parent Node 
        self.HowDidIgetHere=None
        
        # set the goal state 
        self.goalState=list(set(range(n*n)))
        
        ## get the 4 edges of the board, so we know which move is not possible 
        self.upEdge=[] 
        self.downEdge=[]
        self.rightEdge=[] 
        self.leftEdge=[] 
        self.calculateEdgeIndexes()
        
    def calculateEdgeIndexes(self):  
        for i in range (self.n): 
            self.upEdge.append(i) 
        
        for i in range(len(self.upEdge)): 
            self.downEdge.append(self.upEdge[i]+(self.n*(self.n-1))) 
        
        for i in range (self.n): 
            self.leftEdge.append(i*self.n) 
            
        for i in range (len(self.leftEdge)): 
            self.rightEdge.append(self.leftEdge[i]+(self.n-1))
            

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])
    
    def displayAfterMoving(self,anyConfig): 
        """ Display this Puzzle state as a n*n board """
        dim=int(math.sqrt(len(anyConfig)))
        for i in range(dim):
            print(anyConfig[3*i : 3*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """ 
        new_config=list(self.config)
        new_blank=new_config.index(0) 
        moveby=-3
        
        if new_blank in self.upEdge: 
            #print (f'operation not allowed at this state') 
            pass
        else:   
            temp=new_config[new_blank+moveby]  
            new_config[new_blank+moveby]=0 
            new_config[new_blank]=temp 
            #print ('up operation completed')    
        
        return new_config
      
    
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """ 
        new_config=list(self.config)
        new_blank=new_config.index(0) 
        moveby=3
        
        if new_blank in self.downEdge: 
            #print (f'operation not allowed at this state') 
            pass
        else:  
            temp=new_config[new_blank+moveby]  
            new_config[new_blank+moveby]=0 
            new_config[new_blank]=temp 
            #print ('down operation completed')  
         
        return new_config
        
      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """ 
        new_config=list(self.config)
        new_blank=new_config.index(0) 
        moveby=-1
        
        if new_blank in self.leftEdge: 
            #print (f'operation not allowed at this state') 
            pass
        else:  
            temp=new_config[new_blank+moveby]  
            new_config[new_blank+moveby]=0 
            new_config[new_blank]=temp 
            #print ('left operation completed')  
        
        return new_config

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """ 
        new_config=list(self.config)
        new_blank=new_config.index(0) 
        moveby=1
        
        if new_blank in self.rightEdge: 
            #print (f'operation not allowed at this state') 
            pass
        else:  
            temp=new_config[new_blank+moveby]  
            new_config[new_blank+moveby]=0 
            new_config[new_blank]=temp 
            #print ('right operation completed')  
        
        return new_config
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children


def findManhattanDistance(num1,num2):
    indexToCoodinates={ 
    0:(0,0), 1:(0,1), 2:(0,2), 3:(1,0), 4:(1,1), 
    5:(1,2), 6:(2,0), 7:(2,1), 8:(2,2)} 
    
    coord1=indexToCoodinates[num1] 
    coord2=indexToCoodinates[num2] 
    
    distance=abs(coord1[0]-coord2[0])+ abs(coord1[1]-coord2[1])
    return distance 


def FindHeuristic(state): 
    heuristic=0 
    for i in range (len(state)):  
        heuristic+=findManhattanDistance(state[i],i) 
   
    return heuristic


## short 1 node expanded
begin_state=  [3,1,2,0,4,5,6,7,8] 

begin_state = list(map(int, begin_state))
board_size  = int(math.sqrt(len(begin_state)))
hard_state  = PuzzleState(begin_state, board_size) 

goalState=hard_state.goalState 

orderOfExpansion=['Up','Down','Left','Right'] 
explored=set()
pq=Q.PriorityQueue() 
pq.put((0,hard_state)) 

while pq.empty() == False: 
    
    priority,current=pq.get() 
    print (f'trying now {current.display()}') 
    
    if current.config==goalState: 
        print (f'Goal state reached ! {current.config}') 
        break 
    else:  
        explored.add(tuple(current.config)) 
        
        fourExpandedNodes=current.expand() 
                        
        for i in range (len(fourExpandedNodes)):    
            if tuple(fourExpandedNodes[i]) not in explored: 
                newState=PuzzleState(fourExpandedNodes[i],board_size)  
                newState.parent=current 
                newState.HowDidIgetHere=orderOfExpansion[i] 
                heuristic=FindHeuristic(newState.config)
                pq.put((heuristic,newState))                     
                
        

























        
        
        
