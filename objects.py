import os
import sys
import select
import tty
import termios
import time
from colors import *

board = []          # The main grid

class Obj:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
brickcol = []

# no brick (match index with color)
brickcol.append('     ')

# brick type 1 (strength=1) with red color
brickcol.append(colors.bg.red + colors.fg.black + '|___|' + colors.reset)

# brick type 2 (strength=2) with green color
brickcol.append(colors.bg.green + colors.fg.black + '|___|' + colors.reset)

# brick type 3 (strength=3) with blue color
brickcol.append(colors.bg.blue + colors.fg.black + '|___|' + colors.reset)

# brick type 4 (strength=infinite) with magenta color
brickcol.append(colors.bg.purple + colors.fg.black + '|___|' + colors.reset)

# brick type 5 (exploding brick) with yellow color
brickcol.append(colors.bg.yellow + colors.fg.black + '|___|' + colors.reset)

# brick type 6 (rainbow brick) with yellow color
brickcol.append(colors.bg.lightgrey + colors.fg.black + '|___|' + colors.reset)
