from langtons_ant import Board, Ant, create_rules, nonlinear_range

import matplotlib.pyplot as plt
import importlib.util
spec = importlib.util.spec_from_file_location("VideoPlot",
                                              "../video-plot/functions.py")
vp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vp)

# create board and run the simulation #########################################
board = Board()
board.addAnt(Ant(board, create_rules("rrrlr"*1), startPosition=(0, 0)))
board.addAnt(Ant(board, create_rules("rlrrrrrll"*1), startPosition=(0, 40)))
Nmoves = 300000

# store certain states to use for video later
indices = nonlinear_range(0, Nmoves, m=50, multiplier=2)
history, moves = [], []
while board.moves < Nmoves:
    board.iterate()  # this iterates all the ants on the board
    if board.moves in indices:
        history.append(board.contents.copy())
        moves.append(board.moves)
board.plot()

''
# create video ################################################################
# convert board states into numpy arrays for plt.imshow
arrays = [board.contentsToArray(s) for s in history]
Nframes = len(indices) + 1
fig, ax = plt.subplots()
ax.axis("off")
plt.tight_layout()
vmin, vmax = board.vMinMax()  # plt.imshow colourmap limits
vp.VideoPlot(fig, Nframes,
             dict(kind="Image", data=[arrays], ax=ax,
                  formatting=dict(vmin=vmin, vmax=vmax)),
             dict(kind="TextStatic", data=[moves], ax=ax,
                  string_template="moves: {}",
                  formatting=dict(backgroundcolor="r")),
             savefig_kwargs=dict(dpi=100),
             delete_images=False,
             ask_overwrite_permission=False,
             )

"""
TODO:
- need to fix ant position and show in plots. Use imshow with red colormap?
- can I store the state for every single move as the game is played (i.e.
  write it to file? JSON? Then I won't run out of memory, and can still sample
  these states and convert later. This means I only have to run the simulation
  once for each set of parameters. Then I can make long, short videos from it.
- can I give separate ants their own colourmaps?
"""

"""
GOOD PATTERNS:
square space fillers:
rrrlr
rlrrrrrll
rlrrrrlllrr

artistic stuff:
rllr
rrll
rrrrrlrrrllr
rrllllrrrlll
rllrlllrrrr
rrrlllrlll
rllrrlllrlrr
rllrrrlrrrr
rlrllrrrr
rlrlrlllllll
rllrrlrrrrrr
#"""
#'''