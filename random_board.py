#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, random, copy


if (len(sys.argv) != 3):
    print()
    print("Usage: %s [seed] [number of random moves]" %(sys.argv[0]))
    print()
    sys.exit(1)

# Class state
# Description: This class represents a particular state of the 8 number puzzle.
class state():
    def __init__(self, input):
        self.xpos = 0
        self.ypos = 0
        self.tiles = [[0 for x in range(3)]for y in range(3)]
        count = 0
        if input == 0:
            self.tiles = [[1,2,3],[4,5,6],[7,8,9]]
        else:
            for i in range(3):
                for j in range (3):
                    self.tiles[i][j] = int(input[count])
                    count += 1
    def left(self):
        if (self.ypos == 0):
            return self
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos-1]
        s.ypos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def right(self):
        if (self.ypos == 2):
            return self
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos+1]
        s.ypos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def up(self):
        if (self.xpos == 0):
            return self
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos-1][s.ypos]
        s.xpos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def down(self):
        if (self.xpos == 2):
            return self
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos+1][s.ypos]
        s.xpos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def __hash__(self):
        return (tuple(self.tiles[0]),tuple(self.tiles[1]),tuple(self.tiles[2]))
    def __str__(self):
        return '%d %d %d\n%d %d %d\n%d %d %d\n'%(
                self.tiles[0][0],self.tiles[0][1],self.tiles[0][2],
                self.tiles[1][0],self.tiles[1][1],self.tiles[1][2],
                self.tiles[2][0],self.tiles[2][1],self.tiles[2][2])
    def copy(self):
        s = copy.deepcopy(self)
        return s

def main():
    
    # Get and properly store input
    random.seed(int(sys.argv[1]))
    number_of_moves = int(sys.argv[2])
    data = sys.stdin.read().split()
    table = state(data)
    x = 0
    
    # Make run moves until at requested amount
    while x < number_of_moves:
        # These moves will be 0,1,2,3 which can each be
        # associated with a particular movement direction
        # (i.e. up, down, left, right).
        move = random.randrange(4)
        if(move == 0):
            if table.up() != None:
                table = table.up()
                x+=1
        elif(move == 1):
            if table.down() != None:
                table = table.down()
                x+=1
        elif(move == 2):
            if table.left() != None:
                table = table.left()
                x+=1
        else:
            if table.right() != None:
                table = table.right()
                x+=1
                
    # Output table            
    print(table)


                
        
main()
