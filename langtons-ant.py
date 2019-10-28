#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 09:46:10 2019

@author: rmn
"""

import numpy as np, matplotlib.pyplot as plt, pandas as pd
from time import sleep
import importlib.util
spec = importlib.util.spec_from_file_location("VideoPlot", "../video-plot/functions.py")
vp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vp)
#foo.MyClass()
#%%

class Board():
    def __init__(self, contents=dict(), *ants):
        self.contents = contents
        self.ants = list(ants)
        self.iterations = 0  # number of iterations made
        self.moves = 0       # number of moves made
        self.history = []

    def setValue(self, x, y, value):
        string = f"{x},{y}"
        self.contents[string] = value

    def getValue(self, x, y):
        string = f"{x},{y}"
        value = self.contents.get(string)
        return value if value else 0

    def xlim(self, contents=None):
        if contents is None:
            contents = self.contents
        xs = [int(s.split(",")[0]) for s in contents.keys()]
        return min(xs), max(xs)

    def ylim(self, contents=None):
        contents = contents if contents else self.contents
        ys = [int(s.split(",")[1]) for s in contents.keys()]
        return min(ys), max(ys)

    def width(self, contents=None):
        contents = contents if contents else self.contents
        xlim = self.xlim(contents)
        return xlim[1] - xlim[0] + 1

    def height(self, contents=None):
        contents = contents if contents else self.contents
        # replace with contents=self.contents
        ylim = self.ylim(contents)
        return ylim[1] - ylim[0] + 1

    def shape(self, contents=None):
        contents = contents if contents else self.contents
        return self.width(contents), self.height(contents)

    def contentsToArray(self, contents):
        array = np.ones(self.shape(contents)) * np.nan
        # calculate x and y offset required
        xOffset = self.xlim(contents)[0]
        yOffset = self.ylim(contents)[0]

        # populate the array with the entries in self.contents
        for key, value in contents.items():
            x, y = [int(i) for i in key.split(",")]
            array[x-xOffset][y-yOffset] = value
        return array

    def asArray(self):
        return self.contentsToArray(self.contents)

    def plot(self, ax=None):
        if ax is None:
            ax = plt.gca()

        array = self.asArray()
        ax.imshow(array, vmin=0)

#        xOffset = self.xlim()[0]
#        yOffset = self.ylim()[0]
#        ax.set_xticks(ax.get_xticks()-xOffset)
#        ax.set_yticks(ax.get_yticks()-yOffset)

    def addAnt(self, ant):
        self.ants.append(ant)

    def iterate(self):
        for ant in self.ants:
            ant.iterate()
            self.moves += 1
            self.history.append(self.contents.copy())
        self.iterations += 1

    def vMinMax(self):
        vmin = 0
        vmax = max(max(ant.rules) for ant in self.ants)
        return vmin, vmax

class Ant():
    def __init__(self, board, rules, startPosition=None):
        self.rules = rules
        self.board = board
        if startPosition:
            self.position = np.array(startPosition)
        else:
            self.position = np.array([0, 0])  # x, y tuple (or NP array)
        self.directions = (
            np.array([-1, 0]),  # up
            np.array([0, 1]),   # right
            np.array([1, 0]),   # down
            np.array([0, -1]),  # left
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

# %% VideoPlot area

board = Board()
#board.addAnt(Ant(board, createRules("rrl")))
"""redundant: if I'm saying board.addAnt(Ant(board...)) then there's no need to
mention "board" again. There's only one board this ant can be on---the one it
just got added to!"""
#Ant(board, createRules("rrl"))
board.addAnt(Ant(board, createRules("rllr"*9), startPosition=(0,0)))
#board.addAnt(Ant(board, createRules("rrll"), startPosition=(100,5)))
while board.moves < 50000:
    board.iterate()
#%%
Nframes = 200
#indices = np.linspace(0, len(board.history)-1, Nframes).astype(int)
#indices = np.logspace(0, 2, Nframes)
#indices = indices * (len(board.history)-1)/indices[-1]
#indices = indices.astype(int)

indices = np.array([1.05**i-1 for i in range(Nframes)])
indices = indices * ((len(board.history)-1) / indices[-1])
indices = indices.astype(int)
print(indices[:10])
plt.plot(indices, "-ok")
#%%

states = [board.history[i] for i in indices]
arrays = [board.contentsToArray(s) for s in states]
fig, ax = plt.subplots()
ax.axis("off")
plt.tight_layout()
vmin, vmax = board.vMinMax()
vp.VideoPlot(fig, Nframes,
             dict(kind="Image", data=[arrays], ax=ax,
                  formatting=dict(vmin=vmin, vmax=vmax)),
             dict(kind="TextStatic", data=[indices], ax=ax,
                  string_template="moves: {}"),
             savefig_kwargs=dict(dpi=100),
             delete_images=True,
             ask_overwrite_permission=False,
             )

"""NOTE: using board.contentsToArray with the final board means the array will
always be as large as the final board (it uses the height,width of the board
instance, not the array/contents.

NOTE: the VIdeoPlot Image class does plt.imshow on the first data "point" but
then just updates the data on that first point. This results in the colormap
not updating. So any later data values that exceed the colour map from the first
state will get clipped.

NOTE: need to manually specify the normalisation for the imshow. Otherwise it
will only be correct if there's at least one of the highest-number rule squares
present!
"""
'''
rules = createRules("rrl"*10)
#rules = createRules("rllrrrlrrrr"*1)
#rules = createRules("rlrrrrlllrr"*1)
#rules = createRules("rlrlrlllllll"*1)
#rules = createRules("rllrrlrrrrrr"*1)
#rules = createRules("rllr"*2)
#rules = {0: dict(nextColour=1, turnDirection=1),
#         1: dict(nextColour=0, turnDirection=-1)}
board = Board()
board.addAnt(Ant(board, rules))
#board.addAnt(Ant(board, createRules("rrlrrlrrlrl"), startPosition=(0, 80)))
Nplots = 6
Ns = [(10**n+10) for n in range(Nplots+1)]
N = Ns[-1]
cols = int(np.sqrt(Nplots))
rows = int(np.ceil(Nplots/cols))
fig, axes = plt.subplots(rows, cols, figsize=(8, 8))
axes = axes.flatten()
for n in range(N):
    board.iterate()
    if n in Ns:
        ax = axes[Ns.index(n)]
        board.plot(ax)
        ax.set_title(f"N = {n}")

plt.tight_layout()

""" TODO:
- implement video plotting with automatic slow/fast bits
"""
#'''