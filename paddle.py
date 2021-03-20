from objects import *

# paddle = ['{====','====}']
chars = ['_','-','=','-','_']

class Paddle(Obj):

    def __init__(self, x, y):
        self.x = x
        self.c = y                  # column no.
        self.y = (self.c+4)//5      # grid cell column no.
        self.size = 2
        self.color = colors.bg.green
        self.update_block(chars)

    score = 0
    life = 3
    time = 0
    grab = 1
    bricks_rem = 0
    play = 0
    level = 1       # change here ----------------------------------------------------------------------------------------------------------------------------------
    setup = False
    shoot = False

    def update_block(self,paddle):
        """update paddle's position in the board"""
        self.board_pos = []
        num_space = (self.c+4) % 5
        itr = 0
        while itr < 5*(self.size+1):
            val = ''
            for k in range(itr, itr+5):
                if (k >= num_space and k < num_space+self.size*5):     # change 10 to size*5
                    char_cnt = (k-num_space)//self.size
                    if char_cnt == 0 or char_cnt == 4:
                        val = val + self.color + colors.fg.lightred + paddle[char_cnt] + colors.reset
                    else:
                        val = val + colors.bg.green + colors.fg.lightred + paddle[char_cnt] + colors.reset
                else:
                    val = val + ' '
            itr = itr + 5
            self.board_pos.append(val)

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
    
    def left(self):
        """doesn't include board reset and set as requires import of brick.py which would create a cycle(error)"""
        self.c = self.c - 1
        self.y = (self.c+4)//5
        self.update_block(chars)

    def right(self):
        """doesn't include board reset and set as requires import of brick.py which would create a cycle(error)"""
        self.c = self.c + 1
        self.y = (self.c+4)//5
        self.update_block(chars)


P = Paddle(30, 46)
