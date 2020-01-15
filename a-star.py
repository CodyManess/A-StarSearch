#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, copy, heapq, math

# Ensures all parameters are filled. Error message otherwise
if (len(sys.argv) != 3):
    print()
    print("Usage: %s [Heuristic] [Cost per Step]" %(sys.argv[0]))
    print()
    sys.exit(1)

# Class Set
# Description: Represents a set of states.
class Set():
    def __init__(self):
        self.thisSet = set()
    def add(self,entry):
        if entry is not None:
            self.thisSet.add(entry.__hash__())
    def length(self):
        return len(self.thisSet)
    def isMember(self,query):
        return query.__hash__() in self.thisSet 
    def printSet(self):
        for x in self.thisSet:
            print('%d %d %d\n%d %d %d\n%d %d %d\n'%(
                x[0][0],x[0][1],x[0][2],
                x[1][0],x[1][1],x[1][2],
                x[2][0],x[2][1],x[2][2]))

# Class state
# Description: This class represents a particular state of the 8 number puzzle.
class state():
    def __init__(self, input):
        self.tiles = [[0 for x in range(3)]for y in range(3)]
        if input == 0:
            self.tiles = [[0,1,2],[3,4,5],[6,7,8]]
            self.xpos = 0
            self.ypos = 0
        else:        
            count = 0
            for i in range(3):
                for j in range (3):
                    self.tiles[i][j] = int(input[count])
                    if int(input[count]) == 0:
                        self.xpos = i
                        self.ypos = j
                    count += 1
    def left(self):
        if (self.ypos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos-1]
        s.ypos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def right(self):
        if (self.ypos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos+1]
        s.ypos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def up(self):
        if (self.xpos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos-1][s.ypos]
        s.xpos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def down(self):
        if (self.xpos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos+1][s.ypos]
        s.xpos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def tilesDisplaced(self, goal):
        sum = 0
        for i in range(3):
            for j in range (3):
                if self.tiles[i][j] != 0 and (goal.tiles[i][j] != self.tiles[i][j]):
                    sum = sum + 1
        return sum
    def manhattanDistance(self, goal):
        sum = 0
        for i in range(0, 3):
            for j in range(0, 3):
                tile = self.tiles[i][j]
                for m in range(0, 3):
                    for n in range(0, 3):
                        if tile == goal.tiles[m][n] and tile != 0:
                            sum += abs(i-m) + abs(j-n)
        return sum
    def __hash__(self):
        return (tuple(self.tiles[0]),tuple(self.tiles[1]),tuple(self.tiles[2]))
    def __str__(self):
        return '%d %d %d\n%d %d %d\n%d %d %d\n'%(
                self.tiles[0][0],self.tiles[0][1],self.tiles[0][2],
                self.tiles[1][0],self.tiles[1][1],self.tiles[1][2],
                self.tiles[2][0],self.tiles[2][1],self.tiles[2][2])
    def isGoal(self, other):
        for i in range(3):
            for j in range (3):
                if self.tiles[i][j] != other.tiles[i][j]:
                    return False
        return True
    def copy(self):
        s = copy.deepcopy(self)
        return s
        
# Class PriorityQueue
# Description:  Priority Queue that stores nodes and organizes them by value
class PriorityQueue():
    def __init__(self):
        self.thisQueue = []
    def push(self, thisNode):
        heapq.heappush(self.thisQueue, (thisNode.val, -thisNode.id, thisNode))
    def pop(self):
        return heapq.heappop(self.thisQueue)[2]
    def isEmpty(self):
        return len(self.thisQueue) == 0
    def length(self):
        return len(self.thisQueue)
  

nodeid = 0
# Class Node
# Description: Holds information about current state, cost, path cost, depth, and the previous node
class Node():
    def __init__(self, val, pathCost, depth, inputTable, previousNode=None):
        global nodeid
        self.id = nodeid
        nodeid += 1
        self.val = val
        self.pathCost = pathCost
        self.depth = depth
        self.table = inputTable
        self.previousNode = previousNode
    def __str__(self):
        return 'Node: id=%d val=%d'%(self.id,self.val)
    def getTable(self):
        return self.table
    def printPath(self):
        path = []
        temp = self
        while temp is not None:
            path.append(temp.table)
            temp = temp.previousNode
        count = len(path)
        while(count != 0):
            print(path[count-1])
            count -= 1
    def getDepth(self):
        count = 0
        temp = self
        while temp is not None:
            count += 1
            temp = temp.previousNode
        return count
           
            
# Function Heuristic
# Description: Calculates the correct heuristic requested from the command line argument
def heuristic(hType, state, goal):
    if hType == 0:
        return 0
    elif hType == 1:
        return state.tilesDisplaced(goal)
    elif hType == 2:
        return state.manhattanDistance(goal)
    elif hType == 3:
        return state.tilesDisplaced(goal) + state.manhattanDistance(goal)
    
def main():
    #Gather input
    hType = int(sys.argv[1])
    stepCost = int(sys.argv[2])
    pathCost = 0
    data = sys.stdin.read().split()
    
    #Set goal, table, closedList, and openList
    goal = state(0)
    currState = state(data)
    closedList = Set()
    openList = PriorityQueue()
    
    #Create first node
    h = heuristic(hType, currState, goal)
    node = Node(h, 0, 0, currState)
    openList.push(node)
    maxNodes = 1
    #Check if openList is empty. If not, checking and expanding
    while(openList.isEmpty() != True):
        
        node = openList.pop()
        currState = node.getTable()
        
        #
        if( closedList.isMember(currState) != False ):
            continue
        
        #Check if current state is goal
        if currState.isGoal(goal) == True:
            break
            
        closedList.add(currState)
        
        #Create children and push onto openList
        if (currState.up() != None) and (closedList.isMember(currState.up()) != True):
            h = heuristic(hType, currState.up(), goal)
            f = node.pathCost + stepCost
            openList.push(Node(h + f, f, node.depth+1, currState.up(), node))
            
        if (currState.down() != None) and (closedList.isMember(currState.down()) != True):
            h = heuristic(hType, currState.down(), goal)
            f = node.pathCost + stepCost
            openList.push(Node(h + f, f, node.depth+1, currState.down(), node))
            
        if (currState.left() != None) and (closedList.isMember(currState.left()) != True):
            h = heuristic(hType, currState.left(), goal)
            pathCost = node.pathCost + stepCost
            openList.push(Node(h + f, f, node.depth+1, currState.left(), node))
            
        if (currState.right() != None) and (closedList.isMember(currState.right()) != True):
            h = heuristic(hType, currState.right(), goal)
            f = node.pathCost + stepCost
            openList.push(Node(h + f, f, node.depth+1, currState.right(), node))
        
        if (closedList.length() + openList.length()) > maxNodes:
            maxNodes = closedList.length() + openList.length()
        
        

    # Print data and path
    print("V=%d" %closedList.length())
    print("N=%d" %maxNodes)
    print("d=%d" %node.getDepth())
    if node.depth == 0:
        print("b=0\n")
    else:
        print("b=%.5f\n" %pow(closedList.length(), 1/node.depth))
    node.printPath()
    
main()