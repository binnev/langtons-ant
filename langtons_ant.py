import numpy as np
import matplotlib.pyplot as plt


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

    def addAnt(self, ant):
        self.ants.append(ant)

    def iterate(self):
        for ant in self.ants:
            ant.iterate()
            self.moves += 1
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
        # if the ant doesn't have this colour (number), wrap it by length of
        # this ant's rules
        nextColour = self.rules[oldColour % len(self.rules)]["nextColour"]
        self.board.setValue(*self.position, nextColour)

        # 2) update direction based on new colour
        turnDirection = self.rules[nextColour]["turnDirection"]
        self.directionIndex += turnDirection
        self.directionIndex %= len(self.directions)  # wrap

        # 3) move to new square
        self.move()


def create_rules(string):
    rules = dict()
    for ruleNo, char in enumerate(string):
        rule = dict(nextColour=(ruleNo+1) % len(string),
                    turnDirection=(1 if char == "r" else -1))
        rules[ruleNo] = rule
    return rules


def nonlinear_range(start, stop, m=10, spacing=1, multiplier=2):
    # base case -- will the remaining numbers fit into the current range
    if stop <= m:
        return list(range(start, stop, spacing))

    # recursive case -- split off the bottom numbers and recurse
    else:
        first = nonlinear_range(start, m, m, spacing)
        last = nonlinear_range(m, stop, int(m*multiplier),
                              int(spacing*multiplier))
        return first + last
