import numpy as np


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
