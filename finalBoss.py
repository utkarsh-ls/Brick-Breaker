from objects import *
from ball import *

# paddle = ['{====','====}']
ufo = []
ufo.append(["     ","     "," \\  _",".-'~~","~~'-.","_   /","     ","     "])      # 1
ufo.append(["     ","     "," .-~ ","\\__/ "," \\__/"," ~-. ","     ","     "])     # 2
ufo.append(["     ","    .","-~   ","(oo) "," (oo)","    ~","-.   ","     "])       # 3
ufo.append(["     ","   (_","____/","/~~\\\\","//~~\\","\\____","__)  ","     "])   # 4
ufo.append(["   _.","-~`  ","     ","     ","     ","     ","   `~","-._  "])       # 5
ufo.append(["  /O=","O=O=O","=O=O=","O=O=O","=O=O=","O=O=O","=O=O=","O=O\\ "])      # 6
ufo.append(["  \\__","_____","_____","_____","_____","_____","_____","___/ "])      # 7
ufo.append(["     ","     ","   \\x"," x x ","x x x"," x/  ","     ","     "])      # 8
ufo.append(["     ","     ","    \\","x_x_x","_x_x_","x/   ","     ","     "])      # 9

bombs = []

class UFO(Obj):

    def __init__(self, x, y):
        self.x = x                  # top row
        self.c = y                  # first (left) column no.
        self.y = (self.c+4)//5      # grid cell column no.
        self.row_size = 9
        self.col_size = 8
        self.health = 100
        self.update_block(ufo)
        # self.color = colors.bg.green
    
    defense1 = True
    defense2 = True
    crit_health1 = 70
    crit_health2 = 30
    
    def update_block(self,paddle):
        """update paddle's position in the board"""
        self.board_pos = []
        num_space = (self.c+4) % 5
        for i in range(self.row_size):
            # for j in range(self.col_size):
            row = []
            itr = 0
            while itr < 5*(self.col_size+1):
                val = ''
                for k in range(itr, itr+5):
                    if (k >= num_space and k < num_space+self.col_size*5):     # change 10 to size*5
                        char_cnt = (k-num_space)
                        no_col = char_cnt//5        # column no.
                        char_cnt = char_cnt%5       # character no. (in string)
                        # if char_cnt == 0 or char_cnt == 4:
                        #     val = val + self.color + colors.fg.lightred + paddle[char_cnt] + colors.reset
                        # else:
                        val = val + colors.bg.black + colors.fg.yellow + ufo[i][no_col][char_cnt] + colors.reset
                    else:
                        val = val + ' '
                itr = itr + 5
                row.append(val)
            self.board_pos.append(row)
            
    def engage(self, board, balls, powerups, bombs, bullets, num):
        """Creates bricks around boss if health falls below crit level"""
        row_num = self.x + self.row_size + 2-num
        for b in balls:
            if b.x == row_num:
                b.x = b.x + num
        for b in powerups:
            if b.x == row_num:
                b.x = b.x + num
        for b in bombs:
            if b.x == row_num:
                b.x = b.x + num
        for b in bullets:
            if b.x == row_num:
                b.x = b.x + num
        for j in range(1,21):
            board[row_num][j] = brickcol[num]

    # def reset_block(self):
    #     """resets paddle's position in the board (for size"""
    #     self.board_pos = []
    #     num_space = (self.c+4) % 5
    #     itr = 0
    #     while itr < 5*(self.size+1):
    #         val = ''
    #         for k in range(itr, itr+5):
    #             if (k >= num_space and k < num_space+self.size*5):     # change 10 to size*5
    #                 val = val + colors.bg.green + colors.fg.lightred + chars[(k-num_space)//self.size] + colors.reset
    #             else:
    #                 val = val + ' '
    #         itr = itr + 5
    #         self.board_pos.append(brickcol[0])
    
    def left(self,ufo):
        """doesn't include board reset and set as requires import of brick.py which would create a cycle(error)"""
        self.c = self.c - 1
        self.y = (self.c+4)//5
        self.update_block(ufo)

    def right(self,ufo):
        """doesn't include board reset and set as requires import of brick.py which would create a cycle(error)"""
        self.c = self.c + 1
        self.y = (self.c+4)//5
        self.update_block(ufo)

class Bomb(Ball):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = -2
        self.vy = 0
        self.collide = 0
        self.update_block()
        self.init_board = brickcol[0]

    ball_type = colors.fg.cyan + 'ꝺ'

    def move(self):
        prev_x = self.x
        prev_y = self.y
        self.x = self.x - self.vx
        
        self.update_block()
        # self.update_path(prev_x,prev_y)
        
    def collisions(self,paddle):
        if self.x >= 30:
            if self.y >= paddle.c and self.y - paddle.c < 5*paddle.size - 1:
                return 2
            else:
                return 1
        return 0

boss = UFO(1,31)