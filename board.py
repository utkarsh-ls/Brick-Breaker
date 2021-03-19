from pattern import *


def moveBricks(board, P, balls):
    """ Function for board grid moving down"""
    temp_board = []
    for i in range(0, 41):
        temp_board.append([brickcol[0]] * 40)
    for i in range(2, 41):
        for j in range (1, 21):
            if board[i-1][j] == brickcol[1] or \
                    board[i-1][j] == brickcol[2] or \
                    board[i-1][j] == brickcol[3] or \
                    board[i-1][j] == brickcol[4] or \
                    board[i-1][j] == brickcol[5] or \
                    board[i-1][j] == brickcol[6]:
                temp_board[i][j] = board[i-1][j]
    for i in range(0, 41):
        board[i] = temp_board[i]
    updateRainbowBrick(board)
    updateExplodingBrick(board)
    # board = temp_board
    # print(len(temp_board), '***********')
    # for i in range(0, len(temp_board)):
    #     print(len(temp_board[i]), '  /=> i')
    for cnt in range (0,P.size+1):
        board[P.x][P.y+cnt] = P.board_pos[cnt]
    
    for B in balls:
        num_count = (B.y+4)//5
        board[B.x][num_count] = B.board_pos
    for j in range(1, 21):
        # print('//////**', board[30][j], '\n')
        if board[30][j] == brickcol[1] or \
                board[30][j] == brickcol[2] or \
                board[30][j] == brickcol[3] or \
                board[30][j] == brickcol[4] or \
                board[30][j] == brickcol[5] or \
                board[30][j] == brickcol[6]:
            P.life = 0
            break
    return board


def Print():
    os.system('clear')
    for i in range(2):
        print("", end='\n')
    print('\tSCORE = ', end='')
    print(P.score, end='\t')
    print('LIFE = ', end='')
    print(P.life, end='\t')
    print('TIME = ', end='')
    print(P.time, end='\t')
    print('LEVEL = ', end='')
    print(P.level, end='\t')
    print('GAME ', end='')
    if P.play:
        print('CONTINUING (Press p to pause)', end='\n')
    else:
        print('PAUSED (Press p to continue)', end='\n')
    print("", end='\n')
    for i in range(3):
        print(" ", end='')
    for i in range(0, 104):
        print(colors.bg.cyan + ' ' + colors.reset, end='')
    # powerups = set(powerups)
    for i in range(0, 30):
        print("", end='\n')
        print(" ", end='')
        print(" ", end='')
        print(" ", end='')
        print(colors.bg.cyan + '  ' + colors.reset, end='')
        # setup()                 # comment later
        for j in range(1, 21):
            val = 0
            # expensive computation
            for p in powerups:
                if i+1 == p.x and j == p.y and p.active == 0:
                    print(p.board_pos, end='')
                    val = 1
                    break

            if val == 0:
                print(board[i+1][j], end='')

        print(colors.bg.cyan + '  ' + colors.reset, end='')

    print('', end='\n')
    for i in range(3):
        print(' ', end='')
    for i in range(0, 104):
        print(colors.bg.cyan + ' ' + colors.reset, end='')
    print(end='\n')

# Print()
