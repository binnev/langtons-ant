#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 09:46:10 2019

@author: rmn
"""

import numpy as np, matplotlib.pyplot as plt
from time import sleep

class Ant():
    def __init__(self, board, rules, startPosition=None):
        self.rules = rules
        self.board = board
        if startPosition:
            self.position = np.array(startPosition)
        else:
            self.position = len(board) // 2  # x, y tuple (or NP array)
        self.directions = (
            np.array([-1, 0]), # up
            np.array([0, 1]),  # right
            np.array([1, 0]),  # down
            np.array([0, -1]), # left
            )
        self.directionIndex = 0

    def direction(self):
        return self.directions[self.directionIndex]

    def move(self):
        self.position += self.direction()

    def applyRule(self, nextColour, turnDirection):
        p = self.position
        self.board[p[0], p[1]] = nextColour
        self.directionIndex += turnDirection
        self.directionIndex %= len(self.directions)  # wrap

    def doCurrentSquare(self):
        p = self.position
        currentColour = self.board[p[0], p[1]]
        rule = self.rules[currentColour]
        self.applyRule(**rule)

    def iterate(self):
        self.move()
        self.doCurrentSquare()

#    def turnRight(self):
#        self.directionIndex += 1
#        self.directionIndex %= len(self.directions)
#        return self.directions[self.directionIndex]
#
#    def turnLeft(self):
#        self.directionIndex += 1
#        self.directionIndex %= len(self.directions)
#        return self.directions[self.directionIndex]

rules = {0:dict(nextColour=1, turnDirection=1),
         1:dict(nextColour=2, turnDirection=-1),
         2:dict(nextColour=0, turnDirection=1)}


history = []
boardSize = 500
board = np.zeros((boardSize, boardSize))
ants = []
ants.append(Ant(board, rules))
#ants.append(Ant(board, rules, startPosition=(30, 30)))
N = 1000000
for i in range(N):
    for a in ants:
        a.iterate()
#        history.append(a.board.copy())

plt.imshow(board, cmap=plt.cm.viridis_r)
#import importlib.util
#spec = importlib.util.spec_from_file_location("module.name", "../video-plot/functions.py")
#foo = importlib.util.module_from_spec(spec)
#spec.loader.exec_module(foo)
##foo.MyClass()

# %%
"""
- the ants should be ON the board. They shouldn't own the board. There should
  be potentially more than one ant per board
- change the board format. Instead of static size array, have a sparse array
  style thing where you only store squares that have been visited. Unlimited
  size; you can convert to array when you want to make a video.
"""
