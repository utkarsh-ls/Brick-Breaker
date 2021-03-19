import random
from objects import *
from paddle import *
from ball import *

powerups = []
powerups_del = []
MAX_POWERUPS = 7
bullets = []

rem_time = [0,0,0,0,0,0,0]

class Powerup(Obj):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    board_pos = brickcol[0]
    active_time = 10
    
    def isCreate(self, vx, vy):                         
        """Checks if powerup is randomly created or not"""
        # prob(of powerup occuring) = a/b
        a = 1
        b = 3
        num = random.randint(1, b)
        if num <= a and len(powerups) < MAX_POWERUPS:
            self.p_type = random.randint(0, 6)
            self.createPower(vx, vy)

    def createPower(self, vx, vy):                      
        """decide type of powerup"""
        # if (self.p_type == 0):
        #     power_up = Power0(self.x, self.y, vx, vy)
        # elif (self.p_type == 1):
        #     power_up = Power1(self.x, self.y, vx, vy)
        # elif (self.p_type == 2):
        #     power_up = Power2(self.x, self.y, vx, vy)
        # elif (self.p_type == 3):
        #     power_up = Power3(self.x, self.y, vx, vy)
        # elif (self.p_type == 4):
        #     power_up = Power4(self.x, self.y, vx, vy)
        # elif (self.p_type == 5):
        #     power_up = Power5(self.x, self.y, vx, vy)
        # else:
        power_up = Power6(self.x, self.y, vx, vy)
        powerups.append(power_up)

    def update(self, pw, i):
        """update the powerup's position and destroy after set time"""
        if pw.time == 0:
            pw.delete(pw,i)
            powerups.remove(pw)
            # powerups_del.append(i)
        else:
            if (pw.vx > 0):
                pw.x = pw.x - pw.vx
                if(pw.x <= 1):
                    pw.x = 1
                    pw.vx = (-1)*self.vx
                if (pw.vy > 0):
                    pw.y = pw.y + pw.vy
                    if(pw.y >= 20):
                        pw.y = 20
                        pw.vy = (-1)*pw.vy
                else:
                    pw.y = pw.y + pw.vy
                    if(pw.y <= 1):
                        pw.y = 1
                        pw.vy = (-1)*pw.vy
            elif pw.x < 30:
                pw.x = pw.x - pw.vx
                if pw.x > 30:
                    pw.x = 30
                if (pw.vy > 0):
                    pw.y = pw.y + pw.vy
                    if(pw.y >= 20):
                        pw.y = 20
                        pw.vy = (-1)*pw.vy
                else:
                    pw.y = pw.y + pw.vy
                    if(pw.y <= 1):
                        pw.y = 1
                        pw.vy = (-1)*pw.vy
            elif pw.x == 30:
                if pw.y >= P.y and pw.y < P.c+P.size and board[pw.x][pw.y] != brickcol[0]:
                    pw.action()
                    pw.x = pw.x+1
                else:
                    powerups.remove(pw)
                    # powerups_del.append(i)
            elif pw.x == 31:
                if type(pw) == Power5:  # for repeated switch of paddle.grab to 1
                    pw.action()
                elif type(pw) == Power6:
                    pw.action()

                    
    def delete(self, pw, i):
        """delete the powerup"""
        pw.undo_action()
        powerups.remove(pw)
        # powerups_del.append(i)

    def timeLeft(self,pw):
        """remaining time for active powerups"""
        if type(pw) == Power0:
            rem_time[0] = max(rem_time[0]-1,pw.time)
        elif type(pw) == Power1:
            rem_time[1] = max(rem_time[1]-1,pw.time)
        elif type(pw) == Power3:
            rem_time[3] = max(rem_time[3]-1,pw.time)
        elif type(pw) == Power4:
            rem_time[4] = max(rem_time[4]-1,pw.time)
        elif type(pw) == Power5:
            rem_time[5] = max(rem_time[5]-1,pw.time)
        elif type(pw) == Power6:
            rem_time[6] = max(rem_time[6]-1,pw.time)
            

class Power0(Powerup):
    """Power up for expand paddle"""
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.time = self.active_time
    
    active = 0
    board_pos = colors.bg.black + colors.bold + \
        colors.fg.yellow + ' <=> ' + colors.reset

    def action(self):
        if P.size <= 2 and rem_time[0] == 0:
            for cnt in range(0, P.size+1):
                board[P.x][P.y+cnt] = brickcol[0]
            P.size = P.size + 1
            P.update_block(chars)
            for cnt in range(0, P.size+1):
                board[P.x][P.y+cnt] = P.board_pos[cnt]
        self.active = 1

    def undo_action(self):
        if P.size == 3 and rem_time[0] == 0:
            for cnt in range(0, P.size+1):
                board[P.x][P.y+cnt] = brickcol[0]
            P.size = P.size - 1
            P.update_block(chars)
            for cnt in range(0, P.size+1):
                board[P.x][P.y+cnt] = P.board_pos[cnt]


class Power1(Powerup):
    """Power up for shrink paddle"""
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.time = self.active_time
    
    active = 0
    board_pos = colors.bg.black + colors.bold + \
        colors.fg.yellow + ' >=< ' + colors.reset

    def action(self):
        if P.size >= 2 and rem_time[1] == 0:
            for cnt in range(0, P.size+1):
                board[P.x][P.y+cnt] = brickcol[0]
            P.size = P.size - 1
            P.update_block(chars)
            for cnt in range(0, P.size+1):
                board[P.x][P.y+cnt] = P.board_pos[cnt]
        self.active = 1

    def undo_action(self):
        if P.size == 1 and rem_time[1] == 0:
            for cnt in range(0, P.size+1):
                board[P.x][P.y+cnt] = brickcol[0]
            P.size = P.size + 1
            P.update_block(chars)
            for cnt in range(0, P.size+1):
                board[P.x][P.y+cnt] = P.board_pos[cnt]


class Power2(Powerup):
    """Power up for ball multiplier"""
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.time = 1e9
    
    active = 0
    board_pos = colors.bg.black + ' ⊚x2 ' + colors.reset

    def action(self):
        temp_balls = []
        if len(balls)>3:
            return
        for b in balls:
            newBall = Ball(b.x, b.y, -b.vx, -b.vy)
            temp_balls.append(newBall)
        for b in temp_balls:
            balls.append(b)
        self.active = 1

    def undo_action(self):
        return


class Power3(Powerup):
    """Power up for speed ball"""
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.time = self.active_time
    
    active = 0
    board_pos = colors.bg.black + colors.bold + \
        colors.fg.yellow + ' >>> ' + colors.reset

    def action(self):
        if rem_time[3] == 0:
            for B in balls:
                sy = 1
                sx = 1
                if B.vy < 0:
                    sy = -1
                if B.vx < 0:
                    sx = -1
                B.vy = B.vy + sy
                B.vx = B.vx + sx
        self.active = 1

    def undo_action(self):
        # B.vx = B.vx//2
        if rem_time[3] == 0:
            for B in balls:
                sy = 1
                sx = 1
                if B.vy < 0:
                    sy = -1
                if B.vx < 0:
                    sx = -1
                B.vx = B.vx - sx
                B.vy = B.vy - sy


class Power4(Powerup):
    """Power up for through ball"""
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.time = self.active_time
    
    active = 0
    board_pos = colors.bg.black + ' ' + colors.strikethrough + \
        '>[]' + colors.reset + colors.bg.black + ' ' + colors.reset

    def action(self):
        for B in balls:
            B.through = 1
            B.ball_type = colors.fg.yellow + '⊚' + colors.reset
            self.active = 1

    def undo_action(self):
        if rem_time[4] == 0:
            for B in balls:
                B.through = 0
                B.ball_type = colors.fg.lightgrey + '⊚' + colors.reset


class Power5(Powerup):
    """Power up for magnet"""
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.time = self.active_time
    
    active = 0
    board_pos = colors.bg.black + colors.bold + \
        ' |_| ' + colors.reset

    def action(self):
        P.grab = 1
        self.active = 1

    def undo_action(self):
        if rem_time[5] == 0:
            P.grab = 0
        
class Power6(Powerup):
    """Power up for shooting paddle"""
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.time = self.active_time
    
    active = 0
    board_pos = colors.bg.black + colors.bold + \
        ' ↑↑↑ ' + colors.reset
        
    def action(self):
        if rem_time[6] == 0:
            cannon = ['|','-','=','-','|']
            P.color = colors.bg.red
            P.update_block(cannon)
            for cnt in range(0, P.size+1):
                board[P.x][P.y+cnt] = P.board_pos[cnt]
            P.shoot = True
        self.active = 1

    def undo_action(self):
        if rem_time[6] == 0:
            P.color = colors.bg.green
            P.update_block(chars)
            for cnt in range(0, P.size+1):
                board[P.x][P.y+cnt] = P.board_pos[cnt]
            P.shoot = False
            
class Bullet(Ball):
    """Bulllet's for the shooting paddle powerup"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 4
        self.vy = 0
        self.collide = 0
        self.update_block()
    
    ball_type = colors.bg.red + colors.fg.lightgrey + '↑' + colors.reset
    
    def move(self):
        prev_x = self.x
        prev_y = self.y
        self.x = self.x - self.vx
       
        self.update_block()
        self.update_path(prev_x,prev_y)