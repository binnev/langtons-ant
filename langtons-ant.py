#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 09:46:10 2019

@author: rmn
"""

import numpy as np, matplotlib.pyplot as plt
from time import sleep
#import importlib.util
#spec = importlib.util.spec_from_file_location("module.name", "../video-plot/functions.py")
#foo = importlib.util.module_from_spec(spec)
#spec.loader.exec_module(foo)
##foo.MyClass()

class Board():
    def __init__(self):
        self.contents = dict()

    def setValue(self, x, y, value):
        string = f"{x},{y}"
        self.contents[string] = value

    def getValue(self, x, y):
        string = f"{x},{y}"
        value = self.contents.get(string)
        return value if value else 0

    def xlim(self):
        xs = [int(s.split(",")[0]) for s in self.contents.keys()]
        return min(xs), max(xs)

    def ylim(self):
        ys = [int(s.split(",")[1]) for s in self.contents.keys()]
        return min(ys), max(ys)

    def width(self):
        xlim = self.xlim()
        return xlim[1] - xlim[0] + 1

    def height(self):
        ylim = self.ylim()
        return ylim[1] - ylim[0] +1

    def shape(self):
        return self.width(), self.height()

    def asArray(self):
#        array = np.zeros(self.shape())
        array = np.ones(self.shape()) * np.nan
        # calculate x and y offset required
        xOffset = self.xlim()[0]
        yOffset = self.ylim()[0]

        # populate the array with the entries in self.contents
        for key, value in self.contents.items():
            x, y = [int(i) for i in key.split(",")]
            array[x-xOffset][y-yOffset] = value
        return array

    def plot(self, ax=None):
        if ax is None:
            ax = plt.gca()

        array = self.asArray()
        ax.imshow(array, vmin=0)

class Ant():
    def __init__(self, board, rules, startPosition=None):
        self.rules = rules
        self.board = board
        if startPosition:
            self.position = np.array(startPosition)
        else:
            self.position = np.array([0, 0])  # x, y tuple (or NP array)
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

    def iterate(self):
        # 1) change colour of square
        oldColour = self.board.getValue(*self.position)
        nextColour = self.rules[oldColour]["nextColour"]
        self.board.setValue(*self.position, nextColour)

        # 2) update direction based on new colour
        turnDirection = self.rules[nextColour]["turnDirection"]
        self.directionIndex += turnDirection
        self.directionIndex %= len(self.directions)  # wrap

        # 3) move to new square
        self.move()

def createRules(string):
    rules = dict()
    for ruleNo, char in enumerate(string):
        rule = dict(nextColour=(ruleNo+1) % len(string),
                    turnDirection=(1 if char=="r" else -1))
        rules[ruleNo] = rule
    return rules

#rules = createRules("rlrrrrrll"*1)
rules = createRules("rlrrrrlllrr"*1)
#rules = {0: dict(nextColour=1, turnDirection=1),
#         1: dict(nextColour=0, turnDirection=-1)}
board = Board()
ants = []
ants.append(Ant(board, rules))
#ants.append(Ant(board, rules, startPosition=(30, 30)))
N = 500000
for i in range(N):
    for a in ants:
        a.iterate()

board.plot()

""" TODO:
- implement video plotting with automatic slow/fast bits
"""