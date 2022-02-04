#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 18:22:44 2021

@author: Reaz
"""


from __future__ import division
from __future__ import print_function

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
        self.solutionFound=False
        
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
            return []
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
            return []
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
            return []
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
            return []
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
   
    
class Node:
   def __init__(self, value):
      self.value = value
      self.next = None
 
class MyStack:
    
   # Initializing a stack.
   # Use a dummy node, which is
   # easier for handling edge cases.
   def __init__(self):
      self.head = Node("head")
      self.size = 0
 

  
    
   # Check if the stack is empty
   def isEmpty(self):
      return self.size == 0
    

  
   # Push a value into the stack.
   def append(self, value):
      node = Node(value)
      node.next = self.head.next
      self.head.next = node
      self.size += 1
      
   # Remove a value from the stack and return.
   def pop(self):
      if self.isEmpty():
         raise Exception("Popping from an empty stack")
      remove = self.head.next
      self.head.next = self.head.next.next
      self.size -= 1
      return remove.value 
    
    
#def dfs_search(initial_state): 
#    """DFS search"""
#    ### STUDENT CODE GOES HERE ###  
#    def dfs_helper(current_state,goalState,board_size,parentFoundSolution): 
#        print (f'trying now {current_state.config}')
#        if current_state.config==goalState:  
#            print (f'found goal state')             
#            return current_state  
#        
#        elif current_state.config==[]: 
#            return
#        
#            
#        else:  
#            upState=PuzzleState(current_state.move_up(), board_size) 
#            dfs_helper(upState,goalState,board_size,current_state.solutionFound)   
#            
#            downState=PuzzleState(current_state.move_down(), board_size) 
#            dfs_helper(downState,goalState,board_size,current_state.solutionFound)   
#            
#            leftState=PuzzleState(current_state.move_left(), board_size) 
#            dfs_helper(leftState,goalState,board_size,current_state.solutionFound)   
#            
#            rightState=PuzzleState(current_state.move_right(), board_size) 
#            dfs_helper(rightState,goalState,board_size,current_state.solutionFound) 
#            
#    goalState=initial_state.goalState  
#    board_size=int(math.sqrt(len(goalState))) 
#    dfs_helper(initial_state,goalState,board_size,initial_state.solutionFound)
#    
#    
    
def reconstruct_path_for_bfs(goal): 
    path=[]
    current=goal
    while current.parent !=None:  
        path.append(current.HowDidIgetHere)
        current=current.parent 
    
    return list(reversed(path))
            
       
start_time  = time.time()

##short below
#begin_state=  [3,1,2,0,4,5,6,7,8]

## long below (181k) 31
begin_state=  [1,2,5,3,4,0,6,7,8] 

## long below (51k) 28,289
#begin_state=  [ 6,1,8,4,0,2,7,3,5] 

## long below (10k)
#begin_state=  [8,6,4,2,1,3,5,7,0]

begin_state = list(map(int, begin_state))
board_size  = int(math.sqrt(len(begin_state))) 
hard_state  = PuzzleState(begin_state, board_size) 

#stack=MyStack() 
stack=[]
stack.append(hard_state) 
goalState=hard_state.goalState 
explored=set() 
nodes=0 

#while (nodes<10): 
while (len(stack)!=0):
#while (stack.isEmpty() == False): 
    current=stack.pop()  
    print (f'nodes expanded {nodes}')
    print (f'{current.HowDidIgetHere}') 
    print (f'{current.display()}')
    if current.config == goalState: 
        print (f'goal state found {current.config}') 
        break 
    
    tupledConfig=tuple(current.config)
    if (tupledConfig not in explored) : 
        explored.add(tupledConfig)
    
        nodes+=1
        right=current.move_right()         
        if right!=[]:   
            rightState=PuzzleState(right, board_size) 
            rightState.HowDidIgetHere='Right' 
            rightState.parent=current
            if (tuple(right) not in explored) and (rightState not in stack):
                stack.append(rightState) 
                #explored.add(tuple(right))
        
        left=current.move_left() 
        if left!=[]:   
            leftState=PuzzleState(left, board_size) 
            leftState.HowDidIgetHere='Left'
            leftState.parent=current
            if tuple(left) not in explored and (leftState not in stack):
                stack.append(leftState)  
                #explored.add(tuple(left))
        
        down=current.move_down() 
        if down!=[]:   
            downState=PuzzleState(down, board_size) 
            downState.HowDidIgetHere='Down'
            downState.parent=current
            if tuple(down) not in explored and (downState not in stack):
                stack.append(downState)  
                #explored.add(tuple(down))
            
        up=current.move_up() 
        if up!=[]:   
            upState=PuzzleState(up, board_size) 
            upState.HowDidIgetHere='Up'
            upState.parent=current
            if tuple(up) not in explored and (upState not in stack):
                stack.append(upState)  
                #explored.add(tuple(up))

    
    
  
    
    
    

path=reconstruct_path_for_bfs(current) 
print (path)

end_time = time.time()
print("Program completed in %.3f second(s)"%(end_time-start_time)) 

