from objects import *
from powerup import *

# store bricks which will explode 1
bricks1 = []
bricks2 = []

# store rainbow bricks
r_bricks = []

class Brick(Obj):
    """Class for normal bricks"""
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.bricks_broken = 0
    
    def brick_breaker(self,col,vx,vy,board,powerups,fire):
        """For breaking bricks"""
        if not (P.level == 3 and vx < 13):
        # if 1:
                powerup = Powerup(self.x,self.y)
                sy = 0
                if vy > 0:
                    sy = 1
                if vy < 0:
                    sy = -1
                powerup.isCreate(vx,sy*(abs(vy)+4)//5,powerups)
        if fire == 0:
            board[self.x][self.y] = brickcol[col-1]
        else:
            for i in range (self.x-1,self.x+2):
                for j in range (self.y-1, self.y+2):
                    if board[i][j] == brickcol[1] or \
                            board[i][j] == brickcol[2] or \
                            board[i][j] == brickcol[3] or \
                            board[i][j] == brickcol[4] or \
                            board[i][j] == brickcol[6]:
                        board[i][j] = brickcol[0]
                        self.bricks_broken += 1
                    elif board[i][j] == brickcol[5]:
                        brick = Brick5(self.x, self.y)
                        if self.y < 10:
                            brick.explode_bricks(
                                bricks1, vx, vy, board, powerups)
                        else:
                            brick.explode_bricks(
                                bricks2, vx, vy, board, powerups)
                        self.bricks_broken += brick.bricks_exploded

class Brick6(Obj):
    """Class for rainbow bricks"""
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.rainbow = 1
    
    def changeColor(self,board):
        """For changing brick color"""
        if self.rainbow == 1:
            col = random.randint(1, 4)
            board[self.x][self.y] = brickcol[col]
        
    def setColor(self):
        """For fixing color of rainbow brick"""
        self.rainbow = 0

class Brick5(Obj):
    """Class for exploding bricks"""
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.bricks_exploded = 0
    
    def explode_bricks(self,bricks,vx,vy,board,powerups):
        """For exploding bricks near the exploding brick"""    
        for brick in bricks:
            if board[brick[0]][brick[1]] != brickcol[0]:
                for r_brick in r_bricks:
                    if r_brick.x == brick[0] and r_brick.y == brick[1]:
                        r_brick.setColor()
                board[brick[0]][brick[1]] = brickcol[0]
                self.bricks_exploded = self.bricks_exploded + 1
        powerup = Powerup(brick[0],brick[1])                                # change here ------------------------------------------------------------------
        sy = 0
        if vy > 0:
            sy = 1
        if vy < 0:
            sy = -1
        powerup.isCreate(vx,sy*(abs(vy)+4)//5,powerups)
