import random
from objects import *
from paddle import *

balls = []

class Ball(Obj):

    def __init__(self,x,y,vx,vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.update_block()
        self.paddle_touch = 0
        if P.x == self.x+1 and self.y >= P.c and self.y < P.c + 5*P.size:
            self.paddle_touch = 1

    ball_type = colors.fg.lightgrey + '⊚'
    through = 0
    
    def update_block(self):
        """update ball's position in the board"""
        self.board_pos = colors.bold
        num_space = (self.y+4) % 5
        for k in range(0, 5):
            if (k == num_space):
                self.board_pos = self.board_pos + self.ball_type
            else:
                self.board_pos = self.board_pos + ' '
        self.board_pos = self.board_pos + colors.reset

    path=[]

    # def up(self):
    #     if self.x > 2:
    #         self.x = self.x - 2
    #         self.update_block()

    # def down(self):
    #     # if self.x < 19:
    #     self.x = self.x + 1
    #     self.update_block()

    def left(self):
        if self.y > 1:
            self.y = self.y - 1
            self.update_block()

    def right(self):
        if self.y < 100:
            self.y = self.y + 1
            self.update_block()
    
    def move(self):                         # prone to error
        prev_x = self.x
        prev_y = self.y
        if (self.vx > 0):
            self.x = self.x - self.vx
            if(self.x <= 1):
                self.x = 1
                self.vx = (-1)*self.vx
        else:
            self.x = self.x - self.vx
            # if(self.x >= 30):             # change later (ball drops out of map) (comment)
            #     self.x = 30
            #     self.vx = (-1)*self.vx

        if (self.vy > 0):
            self.y = self.y + self.vy
            if(self.y >= 100):
                self.y = 100
                self.vy = (-1)*self.vy
        else:
            self.y = self.y + self.vy
            if(self.y <= 1):
                self.y = 1
                self.vy = (-1)*self.vy
        
        self.update_block()
        self.update_path(prev_x,prev_y)

    def update_path(self,prev_x,prev_y):
        
        self.path = []
        dx = self.x - prev_x        # same as vx if not collided with wall
        dy = self.y - prev_y
        nx = abs(dx)
        ny = abs(dy)
        sx = 1 if dx > 0 else -1
        sy = 1 if dy > 0 else -1
        px = prev_x
        py = prev_y
        ix = 0
        iy = 0

        self.path.append([prev_x,(prev_y+4)//5])
        while (ix<nx or iy<ny):
            decision = (2*ix + 1)*ny - (2*iy + 1)*nx
            if decision == 0:
                px = px+sx
                py = py+sy
                ix = ix + 1
                iy = iy + 1
            elif decision < 0:
                px = px + sx
                ix =  ix + 1
            else:
                py = py + sy
                iy = iy + 1
            self.path.append([px,(py+4)//5])
        
        for x in self.path:
            if self.path.count(x) > 1:
                self.path.remove(x)
    
    def collisions(self,x,prev_x):
        """Handles ball's collision with the paddle/bricks"""
        if prev_x[0] != x[0] and prev_x[1] != x[1]:     # collision at corner
            if  self.through==0:
                self.y = prev_x[1]*5
                self.x = prev_x[0]
                if(self.vy < 0):
                    self.y = self.y - 4
                self.vx = (-1)*self.vx
                self.vy = (-1)*self.vy
        elif prev_x[0] != x[0]:                         # collision with horizontal surface
            var = 1
            for i in range(0, P.size+1):                # for paddle collision
                if board[x[0]][x[1]-i] == P.board_pos[0] and board[x[0]][x[1]-i+1] == P.board_pos[1]:
                    self.y = self.y + (self.vy*(self.x-prev_x[0]))//self.vx
                    self.x = prev_x[0]
                    self.vx = (-1)*self.vx
                    d_vy = self.y - P.c
                    self.vy = self.vy + d_vy//P.size - 2
                    var = 0
                    break
            if self.through==0 and var:
                self.y = self.y + (self.vy*(self.x-prev_x[0]))//self.vx
                self.x = prev_x[0]
                self.vx = (-1)*self.vx
                # var = 2
        elif prev_x[1] != x[1]:                         # collision with vertical surface
            if self.through==0:
                self.y = prev_x[1]*5
                self.x = prev_x[0]
                if(self.vy < 0):
                    self.y = self.y - 4
                self.vy = (-1)*self.vy
                # var = 3

y = random.randint(P.c,P.c+5*P.size-1)
B = Ball(29,y,1,(y-P.c)//P.size - 2)
balls.append(B)
# B = Ball(28,49,-2,4)
