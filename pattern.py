# from colorama import Fore, Back, Style
from brick import *
from paddle import *
from ball import *
from finalBoss import *

# print('Hello', colors.bg.red, colors.fg.black, 'noonno', colors.reset)
# print(brickcol[1])
# print(brickcol[2])
# print(brickcol[3])

def setup1(board):
    P.bricks_rem = 64
    board.clear()
    bricks1.clear()
    bricks2.clear()
    r_bricks.clear()
    for i in range(0, 41):
        board.append([brickcol[0]] * 40)
    
    for i in range(11, 15):
        # rainbow bricks
        board[i][3] = brickcol[6]
        board[i][18] = brickcol[6]
        r_bricks.append(Brick6(i,3))
        r_bricks.append(Brick6(i,18))
        
        # infinte strength bricks
        board[i][10] = brickcol[4]
        board[i][11] = brickcol[4]
    
    for j in range(4, 8):
        # brick type 1
        board[14][j] = brickcol[1]
        board[14][j+10] = brickcol[1]
        
        # brick type 2
        board[11][j] = brickcol[2]
        board[11][j+10] = brickcol[2]
        
    # brick type 3
    for j in range(8, 14):
        if j!=10 and j!=11:
            board[11][j] = brickcol[3]
            board[14][j] = brickcol[3]
        
    # exploding bricsks
    for j in range(4, 10):
        board[12][j] = brickcol[5]
        board[13][j] = brickcol[5]
        board[12][j+8] = brickcol[5]
        board[13][j+8] = brickcol[5]
    for i in range(11, 15):
        for j in range(3, 11):
            bricks1.append([i,j])
            bricks2.append([i,j+8])

    for cnt in range (0,P.size+1):
        board[P.x][P.y+cnt] = P.board_pos[cnt]
    
    for B in balls:
        num_count = (B.y+4)//5
        board[B.x][num_count] = B.board_pos

def setup2(board):
    P.bricks_rem = 126
    board.clear()
    bricks1.clear()
    bricks2.clear()
    r_bricks.clear()
    for i in range(0, 41):
        board.append([brickcol[0]] * 40)
    
    for i in range(6, 11):
        board[i][3] = brickcol[2]
        board[i][18] = brickcol[2]
        if(i < 9):
            for j in range(15-i, i+7):
                board[i][j] = brickcol[3]
                board[i+11][j] = brickcol[3]
        else:
            for j in range(i-1, 23-i):
                board[i][j] = brickcol[3]
                board[i+11][j] = brickcol[3]
    board[11][3] = brickcol[4]
    board[11][18] = brickcol[4]
    for j in range(4, 18):
        board[11][j] = brickcol[2]
    
    # rainbow bricks
    for i in range(12, 16):
        board[i][3] = brickcol[6]
        board[i][18] = brickcol[6]
        r_bricks.append(Brick6(i,3))
        r_bricks.append(Brick6(i,18))
    
    ######## exploding bricks starts
    for j in range (4, 8):
        board[13][j] = brickcol[5]
        board[13][j+10] = brickcol[5]
        board[14][j] = brickcol[5]
        board[14][j+10] = brickcol[5]
        bricks1.append([12,j])
        bricks1.append([13,j])
        bricks1.append([14,j])
        bricks1.append([15,j])
        bricks2.append([12,j+10])
        bricks2.append([13,j+10])
        bricks2.append([14,j+10])
        bricks2.append([15,j+10])
    for i in range(12, 16):
        bricks1.append([i,3])
        bricks1.append([i,8])
        bricks2.append([i,13])
        bricks2.append([i,18])
    ######## exploding bricks ends
    
    for j in range (4, 8):
        board[12][j] = brickcol[4]
        board[12][j+10] = brickcol[4]
        board[15][j] = brickcol[4]
        board[15][j+10] = brickcol[4]

    for i in range(12, 17):
        board[i][8] = brickcol[2]
        board[i][13] = brickcol[2]
    board[16][9] = brickcol[2]
    board[16][12] = brickcol[2]
    
    for j in range(9, 13):
        board[12][j] = brickcol[1]
        board[13][j] = brickcol[1]
        board[15][j] = brickcol[1]
    board[14][9] = brickcol[1]
    board[14][12] = brickcol[1]
    board[16][10] = brickcol[1]
    board[16][11] = brickcol[1]
    
    board[14][10]=brickcol[4]
    board[14][11]=brickcol[4]
    
    for j in range(4, 8):
        board[16][j] = brickcol[1]
        board[16][j+10] = brickcol[1]
    board[16][3] = brickcol[4]
    board[16][18] = brickcol[4]

    for i in range(17, 22):
        board[i][3] = brickcol[1]
        board[i][18] = brickcol[1]

    for j in range(4, 7):
        board[8][j] = brickcol[4]
        board[8][j+11] = brickcol[4]
        board[19][j] = brickcol[4]
        board[19][j+11] = brickcol[4]

    for cnt in range (0,P.size+1):
        board[P.x][P.y+cnt] = P.board_pos[cnt]
    
    for B in balls:
        num_count = (B.y+4)//5
        board[B.x][num_count] = B.board_pos

def setup3(board,ufo):
    P.bricks_rem = 126
    board.clear()
    bricks1.clear()
    bricks2.clear()
    r_bricks.clear()
    for i in range(0, 41):
        board.append([brickcol[0]] * 40)

    for i in range(15, 19):
        # rainbow bricks
        board[i][3] = brickcol[6]
        board[i][18] = brickcol[6]
        r_bricks.append(Brick6(i,3))
        r_bricks.append(Brick6(i,18))
        
        # infinte strength bricks
        board[i][10] = brickcol[4]
        board[i][11] = brickcol[4]
    
    for j in range(4, 8):
        # brick type 1
        board[18][j] = brickcol[1]
        board[18][j+10] = brickcol[1]
        
        # brick type 2
        board[15][j] = brickcol[2]
        board[15][j+10] = brickcol[2]
        
    # brick type 3
    for j in range(8, 14):
        if j!=10 and j!=11:
            board[15][j] = brickcol[3]
            board[18][j] = brickcol[3]
        
    # exploding bricsks
    for j in range(4, 10):
        board[16][j] = brickcol[5]
        board[17][j] = brickcol[5]
        board[16][j+8] = brickcol[5]
        board[17][j+8] = brickcol[5]
    for i in range(15, 19):
        for j in range(3, 11):
            bricks1.append([i,j])
            bricks2.append([i,j+8])


    for i in range(boss.row_size):
        for j in range(boss.col_size+1):
            board[boss.x+i][boss.y+j] = boss.board_pos[i][j]
    
    for cnt in range (0,P.size+1):
        board[P.x][P.y+cnt] = P.board_pos[cnt]
    
    for B in balls:
        num_count = (B.y+4)//5
        board[B.x][num_count] = B.board_pos

# board = setup3(board)
# print(board)

def updateRainbowBrick(board):
    for r_brick in r_bricks:
        r_brick.x += 1
    
def updateExplodingBrick(board):
    for brick in bricks1:
        brick[0] += 1
    for brick in bricks2:
        brick[0] += 1