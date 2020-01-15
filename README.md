# A-Star Search

This is an open lab assignment for CSCI 5350, Intro to Artificial Intelligent.

This goal of this code is to explore the results of using different algorithms on the 8-puzzle problem.

![](https://miro.medium.com/max/1046/1*_n4hcTM-akUEoWL1i05xVg.png)

## a-star.py
a-star.py is a problem-solving software agent that performs A* search for the 8-puzzle problem. a-star.py should read a 8-puzzle board conﬁguration from standard input:

2 8 1\
0 4 3\
7 6 5

and take two arguments(integer: heuristic to use, integer: cost per step).

## random_board.py
Random board.py uses random actions to generate random starting states for the 8-puzzle problem. Random board.py should read the input (the goal) from standard input:

0 1 2\
3 4 5\
6 7 8

accept two arguments (integer: random number generator seed, integer: number of random moves to make), and print a ﬁnal board conﬁguration to standard output in the same format as the input ﬁle format.
