#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 14:52:15 2021

@author: Reaz
"""

## queue Library, explored Set
def bfs_searchLibrary(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###  
    goalState=initial_state.goalState
    frontier=Q.Queue()
    frontier.put(initial_state) 
    explored=set() 
    orderOfExpansion=['Up','Down','Left','Right']
    
    while (frontier.empty()==False): 
        #current=frontier.Pop().data  
        current=frontier.get()
        print (f'Trying now {current.config}')
        if current.config == goalState: 
            print (f'reached Goal state!! {current.config}')
            return current
        else: 
            #if current not in explored: 
            explored.add(tuple(current.config)) 
                #explored.append(current.config)
                
            fourExpandedNodes=current.expand()
            for i in range (len(fourExpandedNodes)):    
                if tuple(fourExpandedNodes[i]) not in explored:
                    newState=PuzzleState(fourExpandedNodes[i], int(math.sqrt(len(fourExpandedNodes[i]))))  
                    newState.parent=current 
                    newState.HowDidIgetHere=orderOfExpansion[i]
                    frontier.put(newState) 
         
 ## CUSTOM QUEUE CLASS, explored Set
def bfs_searchCustom(initial_state):   
    """BFS search"""
    ### STUDENT CODE GOES HERE ###           
    goalState=hard_state.goalState
    frontier= MyQueue()  
    frontier.put(hard_state) 
    explored=set() 
    orderOfExpansion=['Up','Down','Left','Right']
    
    while (frontier.empty()==False): 
        current=frontier.get().data
        print (f'Trying now {current.config}')
        if current.config == goalState: 
            print (f'reached Goal state!! {current.config}')
            return current 
          
        else: 
            explored.add(tuple(current.config))                
            fourExpandedNodes=current.expand()
            
            for i in range (len(fourExpandedNodes)):    
                if tuple(fourExpandedNodes[i]) not in explored: 
                    newState=PuzzleState(fourExpandedNodes[i], int(math.sqrt(len(fourExpandedNodes[i]))))  
                    newState.parent=current 
                    newState.HowDidIgetHere=orderOfExpansion[i]
                    frontier.put(newState) 
            