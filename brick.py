from objects import *
from powerup import *

# store bricks which will explode 1
bricks1 = []
bricks2 = []

# store rainbow bricks
r_bricks = []

class Brick(Obj):
    """Class for normal bricks"""
    def brick_breaker(self,col,vx,vy):
        """For breaking bricks"""
        board[self.x][self.y] = brickcol[col-1]
        if not (level == 3 and vx < 13):
            powerup = Powerup(self.x,self.y)
            powerup.isCreate(vx,(vy+4)//5)
        
class Brick6(Obj):
    """Class for rainbow bricks"""
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.rainbow = 1
    
    def changeColor(self):
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
    
    def explode_bricks(self,bricks,vx,vy):
        """For exploding bricks near the exploding brick"""    
        for brick in bricks:
            if board[brick[0]][brick[1]] != brickcol[0]:
                for r_brick in r_bricks:
                    if r_brick.x == brick[0] and r_brick.y == brick[1]:
                        r_brick.setColor()
                board[brick[0]][brick[1]] = brickcol[0]
                self.bricks_exploded = self.bricks_exploded + 1
        powerup = Powerup(brick[0],brick[1])                                # change here ------------------------------------------------------------------
        powerup.isCreate(vx,(vy+4)//5)
