from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q

import psutil


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

            raise Exception(
                "Config contains invalid/duplicate entries : ", config)

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.config = config
        self.children = []
        self.depth = 0

        # Get the index and (row, col) of empty block

        self.blank_index = self.config.index(0)

        ## declare the parent Node

        self.HowDidIgetHere = None

        # set the goal state
        self.goalState = list(set(range(n*n)))

        ## get the 4 edges of the board, so we know which move is not possible

        self.upEdge = []
        self.downEdge = []
        self.rightEdge = []
        self.leftEdge = []
        self.calculateEdgeIndexes()

    def calculateEdgeIndexes(self):

        for i in range(self.n):
            self.upEdge.append(i)

        for i in range(len(self.upEdge)):
            self.downEdge.append(self.upEdge[i]+(self.n*(self.n-1)))

        for i in range(self.n):
            self.leftEdge.append(i*self.n)

        for i in range(len(self.leftEdge)):
            self.rightEdge.append(self.leftEdge[i]+(self.n-1))

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i: 3*(i+1)])

    def displayAfterMoving(self, anyConfig):
        """ Display this Puzzle state as a n*n board """

        dim = int(math.sqrt(len(anyConfig)))

        for i in range(dim):

            print(anyConfig[3*i: 3*(i+1)])

    def move_up(self):
        """

        Moves the blank tile one row up.

        :return a PuzzleState with the new configuration

        """

        new_config = list(self.config)

        new_blank = new_config.index(0)

        moveby = -3

        if new_blank in self.upEdge:

            #print (f'operation not allowed at this state')

            pass

        else:

            temp = new_config[new_blank+moveby] 

            new_config[new_blank+moveby] = 0

            new_config[new_blank] = temp

            #print ('up operation completed')

        return new_config

    def move_down(self):
        """

        Moves the blank tile one row down.

        :return a PuzzleState with the new configuration

        """

        new_config = list(self.config)

        new_blank = new_config.index(0)

        moveby = 3

        if new_blank in self.downEdge:

            #print (f'operation not allowed at this state')

            pass

        else:

            temp = new_config[new_blank+moveby]

            new_config[new_blank+moveby] = 0

            new_config[new_blank] = temp

            #print ('down operation completed')

        return new_config

    def move_left(self):
        """

        Moves the blank tile one column to the left.

        :return a PuzzleState with the new configuration

        """

        new_config = list(self.config)

        new_blank = new_config.index(0)

        moveby = -1

        if new_blank in self.leftEdge:

            #print (f'operation not allowed at this state')

            pass

        else:

            temp = new_config[new_blank+moveby]

            new_config[new_blank+moveby] = 0

            new_config[new_blank] = temp

            #print ('left operation completed')

        return new_config

    def move_right(self):
        """

        Moves the blank tile one column to the right.

        :return a PuzzleState with the new configuration

        """

        new_config = list(self.config)

        new_blank = new_config.index(0)

        moveby = 1

        if new_blank in self.rightEdge:

            #print (f'operation not allowed at this state')

            pass

        else:

            temp = new_config[new_blank+moveby]

            new_config[new_blank+moveby] = 0

            new_config[new_blank] = temp

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

    def expandInReverseOrder(self):
        """ Generate the child nodes of this node """

        # Node has already been expanded

        if len(self.children) != 0:

            return self.children

        # Add child nodes in order of UDLR

        children = [

            self.move_right(),

            self.move_left(),

            self.move_down(),

            self.move_up()]

        # Compose self.children of all non-None children states

        self.children = [state for state in children if state is not None]

        return self.children

    def calculateDepth(self):

        depth = 0

        if self.parent == None:

            self.depth = 0

            return depth

        else:

            parent = self.parent

            while parent != None:

                depth += 1

                parent = parent.parent

            return depth


## class TextFile Handler to create and edit a text file ##

class TextFileHandler(object):

    def __init__(self, filename):

       self.filename = filename

    def writer(self, content):

        file = open(self.filename, 'w')

        file.write(content)

        file.close()

    def appender(self, content):

        file = open(self.filename, 'a')

        file.write(content)

        file.close()

    def insertEmptyLine(self):

        file = open(self.filename, 'a')

        file.write('\n')

        file.close()

    def writeOutputDictionary(self, outputDictionary):

        self.writer(f"path_to_goal: {outputDictionary['path_to_goal']}")

        self.insertEmptyLine()

        self.appender(f"cost_of_path: {outputDictionary['cost_of_path']}")

        self.insertEmptyLine()

        self.appender(f"nodes_expanded: {outputDictionary['nodes_expanded']}")

        self.insertEmptyLine()

        self.appender(f"search_depth: {outputDictionary['search_depth']}")

        self.insertEmptyLine()

        self.appender(
            f"max_search_depth: {outputDictionary['max_search_depth']}")

        self.insertEmptyLine()

        self.appender(f"running_time: {outputDictionary['running_time']}")

        self.insertEmptyLine()

        self.appender(f"max_ram_usage: {outputDictionary['max_ram_usage']}")


######################## BFS RELATED ####################################


### CUSTOM QUEUE CLASS ###

class MyNode:

    def __init__(self, data):

        self.data = data

        self.next = None


class MyQueue:

    def __init__(self):

        self.front = self.end = None

    def empty(self):

        return self.front == None

    def put(self, element):

        temp = MyNode(element)

        if self.end == None:

            self.front = self.end = temp

            return

        self.end.next = temp

        self.end = temp

    def get(self):

        if self.empty():

            return

        temp = self.front

        self.front = temp.next

        if (self.front == None):

            self.end = None

        return temp


class Bfs_Search(object):

    def __init__(self, initial_state):

        self.outputDictionary = {

            'path_to_goal': 0,

            'cost_of_path': 0,

            'nodes_expanded': 0,

            'search_depth': 0,

            'max_search_depth': 0,

            'running_time': 0,

            'max_ram_usage': 0}

        self.initialState = initial_state

        self.goalState = initial_state.goalState

        self.boardSize = int(math.sqrt(len(initial_state.config)))

        self.frontier = MyQueue()

        self.explored = set()

        self.visitedCombined = {}

        self.orderOfExpansion = ['Up', 'Down', 'Left', 'Right']

        self.frontier.put(initial_state)

    def ReconstructPath(self, goal):

        path = []

        current = goal

        while current.parent != None:

            path.append(current.HowDidIgetHere)

            current = current.parent

        return list(reversed(path))

    def FindMaxDepth(self):

        while self.frontier.empty() == False:

            lastEntry = self.frontier.get().data

        max_depth = 0

        while lastEntry.parent != None:

            max_depth += 1

            lastEntry = lastEntry.parent

        return max_depth

    def FindRamUsage(self):

        ram_use=  round(((psutil.virtual_memory()[2])/100),8)  
        return ram_use

    def BfsAlgorithm(self):

        start_time = time.time()

        while (self.frontier.empty() == False):

            current = self.frontier.get().data

            ## for debug only

            #print (f'nodes expanded {len(self.explored)}')

            if current.config == self.goalState:

                end_time = time.time()

                total_time = round((end_time-start_time), 8)

                ## populate output dictionary

                self.outputDictionary['path_to_goal'] = self.ReconstructPath(
                    current)

                self.outputDictionary['cost_of_path'] = len(
                    self.outputDictionary['path_to_goal'])

                self.outputDictionary['nodes_expanded'] = len(self.explored)

                self.outputDictionary['search_depth'] = len(
                    self.outputDictionary['path_to_goal'])

                self.outputDictionary['max_search_depth'] = self.FindMaxDepth()

                self.outputDictionary['running_time'] = total_time

                self.outputDictionary['max_ram_usage'] = self.FindRamUsage()

               

                return self.outputDictionary

                break

            else:

                tupledCurrentConfig = tuple(current.config)

                if tupledCurrentConfig not in self.explored:

                    self.visitedCombined[tuple(current.config)] = True

                    self.explored.add(tupledCurrentConfig)

                    fourExpandedNodes = current.expand()

                    for i in range(len(fourExpandedNodes)):

                        tupledChild = tuple(fourExpandedNodes[i])

                        if tupledChild not in self.visitedCombined:

                            self.visitedCombined[tupledChild] = True

                            newState = PuzzleState(
                                fourExpandedNodes[i], self.boardSize)

                            newState.parent = current

                            newState.HowDidIgetHere = self.orderOfExpansion[i]

                            self.frontier.put(newState)


###############################################################################################


######################## BFS RELATED ####################################


### CUSTOM STACK CLASS ###


class StackNode(object):

    def __init__(self, data):

        self.value = data

        self.next = None


class MyStack:

   def __init__(self):

      self.head = StackNode("head")

      self.size = 0

   def isEmpty(self):

      return self.size == 0

   def append(self, value):

      node = StackNode(value)

      node.next = self.head.next

      self.head.next = node

      self.size += 1

   def pop(self):

      if self.isEmpty():

         raise Exception("Popping from an empty stack")

      remove = self.head.next

      self.head.next = self.head.next.next

      self.size -= 1

      return remove.value


class Dfs_Search(object):

    def __init__(self, initial_state):

        self.outputDictionary = {

            'path_to_goal': 0,

            'cost_of_path': 0,

            'nodes_expanded': 0,

            'search_depth': 0,

            'max_search_depth': 0,

            'running_time': 0,

            'max_ram_usage': 0}

        self.initialState = initial_state

        self.goalState = initial_state.goalState

        self.boardSize = int(math.sqrt(len(initial_state.config)))

        self.frontier = MyStack()

        self.explored = set()

        self.visitedCombined = {}

        self.orderOfExpansion = ['Right', 'Left', 'Down', 'Up']

        self.max_depth = 0

        self.frontier.append(initial_state)

    def ReconstructPath(self, goal):

        path = []

        current = goal

        while current.parent != None:

            path.append(current.HowDidIgetHere)

            current = current.parent

        return list(reversed(path))

    def FindRamUsage(self):

        ram_use=  round(((psutil.virtual_memory()[2])/100),8)  
        return ram_use

    def DfsAlgorithm(self):

        start_time = time.time()

        while (self.frontier.isEmpty() == False):

            current = self.frontier.pop()

            if current.config == self.goalState:

                end_time = time.time()

                total_time = round((end_time-start_time), 8)

                ## populate output dictionary

                self.outputDictionary['path_to_goal'] = self.ReconstructPath(
                    current)

                self.outputDictionary['cost_of_path'] = len(
                    self.outputDictionary['path_to_goal'])

                self.outputDictionary['nodes_expanded'] = len(self.explored)

                self.outputDictionary['search_depth'] = len(
                    self.outputDictionary['path_to_goal'])

                self.outputDictionary['max_search_depth'] = self.max_depth

                self.outputDictionary['running_time'] = total_time

                self.outputDictionary['max_ram_usage'] = self.FindRamUsage()

                

                return self.outputDictionary

                break

            else:

                tupledCurrentConfig = tuple(current.config)

                if tupledCurrentConfig not in self.explored:

                    self.visitedCombined[tuple(current.config)] = True

                    self.explored.add(tupledCurrentConfig)

                    self.max_depth = max(self.max_depth, current.depth)

                    fourExpandedNodes = current.expandInReverseOrder()

                    for i in range(len(fourExpandedNodes)):

                        tupledChild = tuple(fourExpandedNodes[i])

                        if tupledChild not in self.visitedCombined:

                            self.visitedCombined[tupledChild] = True

                            newState = PuzzleState(
                                fourExpandedNodes[i], self.boardSize)

                            newState.parent = current

                            newState.HowDidIgetHere = self.orderOfExpansion[i]

                            newState.depth = current.depth+1

                            self.max_depth = max(
                                self.max_depth, newState.depth)

                            self.frontier.append(newState)


################################ A STAR RELATED ############################


class Astar_Search(object):

    def __init__(self, initial_state):

        self.outputDictionary = {

            'path_to_goal': 0,

            'cost_of_path': 0,

            'nodes_expanded': 0,

            'search_depth': 0,

            'max_search_depth': 0,

            'running_time': 0,

            'max_ram_usage': 0}

        self.initialState = initial_state

        self.goalState = initial_state.goalState

        self.boardSize = int(math.sqrt(len(initial_state.config)))

        self.frontier = Q.PriorityQueue()

        self.explored = set()

        self.visitedCombined = {}

        self.orderOfExpansion = ['Up', 'Down', 'Left', 'Right']

        self.max_depth = 0

        self.tie_breaker = 0

        self.frontier.put((0, 0, initial_state))

    def ReconstructPath(self, goal):

        path = []

        current = goal

        while current.parent != None:

            path.append(current.HowDidIgetHere)

            current = current.parent

        return list(reversed(path))

    def CalculateMaxDepth(self):

        ##deque the Priority Queue and check if any of the stored depth is larger than the currently found max depth

        while self.frontier.empty() == False:

            priority, tieBreaker, lastFrontier = self.frontier.get()

            self.max_depth = max(self.max_depth, lastFrontier.depth)

        return self.max_depth

    def FindRamUsage(self):

        ram_use=  round(((psutil.virtual_memory()[2])/100),8)  
        return ram_use

    def findManhattanDistance(self, num1, num2):

        indexToCoodinates = {

            0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (1, 0), 4: (1, 1),

            5: (1, 2), 6: (2, 0), 7: (2, 1), 8: (2, 2)}

        coord1 = indexToCoodinates[num1]

        coord2 = indexToCoodinates[num2]

        distance = abs(coord1[0]-coord2[0]) + abs(coord1[1]-coord2[1])

        return distance

    def FindHeuristic(self, state):

        heuristic = 0

        for i in range(len(state)):

            if state[i] != 0:

                heuristic += self.findManhattanDistance(state[i], i)

        return heuristic

    def AstarAlgorithm(self):

        start_time = time.time()

        while (self.frontier.empty() == False):

            priority, tibreak, current = self.frontier.get()

            if current.config == self.goalState:

                end_time = time.time()

                total_time = round((end_time-start_time), 8)

                ## populate output dictionary

                self.outputDictionary['path_to_goal'] = self.ReconstructPath(
                    current)

                self.outputDictionary['cost_of_path'] = len(
                    self.outputDictionary['path_to_goal'])

                self.outputDictionary['nodes_expanded'] = len(self.explored)

                self.outputDictionary['search_depth'] = len(
                    self.outputDictionary['path_to_goal'])

                self.outputDictionary['max_search_depth'] = self.CalculateMaxDepth(
                )

                self.outputDictionary['running_time'] = total_time

                self.outputDictionary['max_ram_usage'] = self.FindRamUsage()

                

                return self.outputDictionary

                break

            else:

                tupledCurrentConfig = tuple(current.config)

                if tupledCurrentConfig not in self.explored:

                    self.explored.add(tupledCurrentConfig)

                    self.visitedCombined[tuple(current.config)] = True

                    if current.depth == 0:

                        current_depth = current.calculateDepth()

                    else:

                        current_depth = current.depth

                    self.max_depth = max(self.max_depth, current_depth)

                    fourExpandedNodes = current.expand()

                    for i in range(len(fourExpandedNodes)):

                        tupled = tuple(fourExpandedNodes[i])

                        if tupled not in self.visitedCombined:

                           self.visitedCombined[tupled] = True

                           newState = PuzzleState(
                               fourExpandedNodes[i], self.boardSize)

                           newState.parent = current

                           newState.HowDidIgetHere = self.orderOfExpansion[i]

                           newState.depth = current_depth+1

                           self.max_depth = max(self.max_depth, newState.depth)

                           heuristic = self.FindHeuristic(newState.config)

                           self.frontier.put(
                               (heuristic+newState.depth, self.tie_breaker, newState))

                           self.tie_breaker += 1

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters


def writeOutput():
    print ('I HAVE IMPLEMENTED THIS FUNCTION IN MY TEXTFILE HANDLER CLASS, THEREFORE NOT REIMPLEMENTING IT HERE AGAIN')
    


def bfs_search(initial_state):
    """BFS search"""
    bfsObject=Bfs_Search(initial_state) 

    outputDict=bfsObject.BfsAlgorithm() 
    
    #print (outputDict)

    outputFileObject=TextFileHandler('output.txt')

    outputFileObject.writeOutputDictionary(outputDict)


def dfs_search(initial_state):
    """DFS search"""
    dfsObject=Dfs_Search(initial_state) 

    outputDict=dfsObject.DfsAlgorithm() 
    #print (outputDict)

    outputFileObject=TextFileHandler('output.txt')

    outputFileObject.writeOutputDictionary(outputDict)


def A_star_search(initial_state):
    """A * search"""
    aStarObject=Astar_Search(initial_state) 

    outputDict=aStarObject.AstarAlgorithm()

    #print (outputDict)
    outputFileObject=TextFileHandler('output.txt')

    outputFileObject.writeOutputDictionary(outputDict)


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    print ('I HAVE IMPLEMENTED THIS METHOD INSIDE MY ASTAR SEARCH CLASS, THEREFORE NOT REIMPLEMENTING IT HERE AGAIN')
    pass


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    print ('I HAVE IMPLEMENTED THIS METHOD INSIDE MY ASTAR SEARCH CLASS, THEREFORE NOT REIMPLEMENTING IT HERE AGAIN')

    pass


def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    print ('I HAVE IMPLEMENTED THIS METHOD INSIDE THE RESPECTIVE SEARCH CLASSES, THEREFORE NOT REIMPLEMENTING IT HERE AGAIN')    

# Main Function that reads in Input and Runs corresponding Algorithm


def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, board_size)
    start_time = time.time()

    if search_mode == "bfs":
        bfs_search(hard_state)
    elif search_mode == "dfs":
        dfs_search(hard_state)
    elif search_mode == "ast":
        A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")

    end_time = time.time()
    print("Program completed in %.3f second(s)" % (end_time-start_time))


if __name__ == '__main__':
    main()
