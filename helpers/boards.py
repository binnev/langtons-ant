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
