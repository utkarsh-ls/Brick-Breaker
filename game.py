#!/usr/bin/python
# -*- coding: utf-8 -*-

# import os
# import sys
# import select
# import tty
# import termios
# import time
from colors import *
from board import *
from input import *
from brick import *
from paddle import *
from ball import *
from powerup import *
from finalBoss import *

# if M.sound == 1:
os.system('spd-say -tfemale3 -r-20 "Welcome to the classic block breaker game" &')

FPS = 4
# For moving bricks down
TIME_QUANTA = 7
# For dropping BOMBS
BOMB_TIME = 7
# ali = []

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [],
                                                     [])


setup1(board)
# P.setup = True     # change later ----------------------------------------------------------------------------------------------------------------------------------------------
Print(powerups)
old_settings = termios.tcgetattr(sys.stdin)
start = time.time()
counter = 0
L3_time = 0
begin = time.time()
try:
    tty.setcbreak(sys.stdin.fileno())
    # setup()     # maybe?
    while 1:
        t0 = time.time() - start

        if (time.time() - begin > 1) and P.play:
            
            # boss music
            if P.level == 3:
                boss_music_time = 52
                if L3_time%boss_music_time == 0:
                    os.system("aplay -q sound/boss_music.wav &")
                L3_time = L3_time + 1
            # update powerup's time
            for i, pw in enumerate(powerups):
                if pw.active == 1:
                    pw.time = pw.time - 1
                    pw.timeLeft(pw)
            # change rainbow brick's color
            if P.time % 3 == 0:
                for r_brick in r_bricks:
                    r_brick.changeColor(board)
            # drop bombs in level 3 (Boss level)
            if P.level == 3 and P.time % BOMB_TIME == BOMB_TIME-1:
                col = random.randint(boss.c, boss.c+5*boss.col_size-1)
                b = Bomb(boss.x+boss.row_size, col)
                bombs.append(b)
            # move bricks down
            t = TIME_QUANTA*(2*P.level-1)
            if P.time % t == t-1:
                board = moveBricks(board, P, balls)
                # P.play = 0
                Print(powerups)

            # for i, pw in enumerate(powerups):
            #    pw.update(pw,i)
            # powerups = [pw for pw in powerups if pw.passive != 1]

            if P.shoot == True:
                bullet = Bullet(P.x-1, P.c)
                # bullet.shoot()
                bullets.append(bullet)
                bullet = Bullet(P.x-1, P.c+P.size*5-1)
                # bullet.shoot()
                os.system("aplay -q sound/bullet.wav &")
                bullets.append(bullet)

            P.time = P.time + 1
            begin = time.time()

        if ((t0*FPS) % 1) < 0.00001 and ((t0*FPS) % 1) > -0.00001 and P.play:
            for B in bombs:
                board[B.x][(B.y+4)//5] = B.init_board
                B.move()
                isCollide = B.collisions(P)

                if isCollide == 2:
                    # bomb collides with paddle decreasing it's life
                    os.system("aplay -q sound/bomb.wav &")
                    P.life = P.life - 1
                    for t in range(len(rem_time)):
                        rem_time[t] = 0
                    for i, pw in enumerate(powerups):
                        pw.delete(pw)
                    # powerups = [pw for pw in powerups if pw.passive != 1]
                    powerups.clear()
                    # -----------------------------------------------------------------
                    balls.clear()
                    bombs.clear()
                    bullets.clear()
                    # -----------------------------------------------------------------
                    P.grab = 1
                    y = random.randint(P.c, P.c+5*P.size-1)
                    B = Ball(29, y, 2, (y-P.c)//P.size - 2)
                    balls.append(B)
                elif isCollide == 1:
                    # (bombs drops out of map)
                    bombs.remove(B)
                else:
                    temp_cell = brickcol[0]
                    for i in range(1, 7):
                        if board[B.x][(B.y+4)//5] == brickcol[i]:
                            temp_cell = brickcol[i]
                    B.init_board = temp_cell
                    board[B.x][(B.y+4)//5] = B.board_pos

            for B in bullets:
                board[B.x][(B.y+4)//5] = brickcol[0]
                B.move()
                prev_x = []
                for x in B.path:
                    if prev_x and board[x[0]][x[1]] == brickcol[1] or \
                            board[x[0]][x[1]] == brickcol[2] or \
                            board[x[0]][x[1]] == brickcol[3] or \
                            board[x[0]][x[1]] == brickcol[4] or \
                            board[x[0]][x[1]] == brickcol[5] or \
                            board[x[0]][x[1]] == brickcol[6]:

                        # for bullet collisions update bricks
                        for i in range(1, 7):
                            if board[x[0]][x[1]] == brickcol[i]:
                                if i == 5:
                                    os.system("aplay -q sound/exploding_brick.wav &")
                                    brick = Brick5(x[0], x[1])
                                    if x[1] < 10:
                                        brick.explode_bricks(
                                            bricks1, B.vx, B.vy, board, powerups)
                                    else:
                                        brick.explode_bricks(
                                            bricks2, B.vx, B.vy, board, powerups)
                                    P.score = P.score + 50*brick.bricks_exploded
                                else:
                                    os.system("aplay -q sound/brick_collision.wav &")
                                    if i <= 3:
                                        rainbow_brick = 0
                                        # rainbow bricks
                                        for r_brick in r_bricks:
                                            if r_brick.x == x[0] and r_brick.y == x[1] and r_brick.rainbow == 1:
                                                rainbow_brick = 1
                                                r_brick.setColor()
                                                break

                                        if rainbow_brick == 0:
                                            brick = Brick(x[0], x[1])
                                            brick.brick_breaker(i, B.vx, B.vy, board, powerups, 0)

                                        P.score = P.score + 10
                                break
                        
                        # for boss collision create defensive bricks
                        if P.level == 3 and boss.defense1 == True and boss.defense2 == True:
                            if x[0] >= boss.x and x[0] < boss.x+boss.row_size:
                                for i in range(boss.row_size):
                                    c = 0
                                    if (boss.c+4) % 5:
                                        c = 1
                                    for j in range(boss.col_size+c):
                                        if board[x[0]][x[1]] == boss.board_pos[i][j]:
                                            boss.health -= (abs(B.vx) +
                                                            abs(B.vy))
                                            if boss.health < 0:
                                                boss.health = 0
                                            if boss.health <= boss.crit_health1 and boss.defense1 == True:
                                                boss.engage(
                                                    board, balls, powerups, bombs, bullets, 1)
                                                boss.defense1 = False
                                            elif boss.health <= boss.crit_health2 and boss.defense2 == True:
                                                boss.engage(
                                                    board, balls, powerups, bombs, bullets, 2)
                                                boss.defense1 = False
                                            break
                        
                        # for bullet collision with brick update bullet (delete)
                        B.collide = 1
                        B.update_block()
                        break
                    prev_x = x

                # (bullet reaches top of map or collides)
                if B.x < 1 or B.collide == 1:
                    bullets.remove(B)
                else:
                    board[B.x][(B.y+4)//5] = B.board_pos

            bricks_rem = 0
            for row in board:
                for b in row:
                    if b == brickcol[1] or b == brickcol[2] or b == brickcol[3]:
                        bricks_rem += 1
            if bricks_rem == 0:
                P.level = P.level + 1
                P.play = 0
                # bombs.clear()
                # bullets.clear()
                # balls.clear()
                # powerups.clear()
                P.setup = True
            if P.play == 0:
                Print(powerups)
                print('\n')
                time.sleep(2)

        if ((t0*FPS) % 1) < 0.00001 and ((t0*FPS) % 1) > -0.00001 and P.play:

            for B in balls:
                if P.grab == 1 and B.x == P.x-1 and B.y >= P.c and B.y < P.c + 5*P.size:
                    continue
                board[B.x][(B.y+4)//5] = brickcol[0]
                B.move()
                prev_x = []
                # ali = []
                for x in B.path:
                    if(prev_x and board[x[0]][x[1]] != brickcol[0]):

                        # for brick collisions update bricks
                        for i in range(1, 7):
                            if board[x[0]][x[1]] == brickcol[i]:
                                if i == 5:
                                    os.system("aplay -q sound/exploding_brick.wav &")
                                    brick = Brick5(x[0], x[1])
                                    if x[1] < 10:
                                        brick.explode_bricks(
                                            bricks1, B.vx, B.vy, board, powerups)
                                    else:
                                        brick.explode_bricks(
                                            bricks2, B.vx, B.vy, board, powerups)
                                    P.score = P.score + 50*brick.bricks_exploded
                                elif B.through == 0 and B.fire == 0:
                                    os.system("aplay -q sound/brick_collision.wav &")
                                    if i <= 4:
                                        rainbow_brick = 0
                                        # rainbow bricks
                                        for r_brick in r_bricks:
                                            if r_brick.x == x[0] and r_brick.y == x[1] and r_brick.rainbow == 1:
                                                rainbow_brick = 1
                                                r_brick.setColor()
                                                break

                                        if rainbow_brick == 0 and i <= 3:
                                            brick = Brick(x[0], x[1])
                                            brick.brick_breaker(i, B.vx, B.vy, board, powerups, 0)

                                        P.score = P.score + 10
                                elif B.fire == 0:
                                    # through ball
                                    brick = Brick(x[0], x[1])
                                    brick.brick_breaker(1, B.vx, B.vy, board, powerups, 0)
                                    P.score = P.score + 10*i
                                else:
                                    # fire ball
                                    os.system("aplay -q sound/exploding_brick.wav &")
                                    rainbow_brick = 0
                                    # rainbow bricks
                                    for r_brick in r_bricks:
                                        if r_brick.x == x[0] and r_brick.y == x[1] and r_brick.rainbow == 1:
                                            rainbow_brick = 1
                                            r_brick.setColor()
                                            P.score = P.score + 10
                                            break

                                    if rainbow_brick == 0:
                                        brick = Brick(x[0], x[1])
                                        brick.brick_breaker(i, B.vx, B.vy, board, powerups, 1)
                                        P.score = P.score + 10*brick.bricks_broken
                                # ali = powerups
                                break

                        # for boss collision create defensive bricks
                        if P.level == 3:
                            if x[0] >= boss.x and x[0] < boss.x+boss.row_size:
                                c = 0
                                if (boss.c+4) % 5:
                                    c = 1
                                for i in range(boss.row_size):
                                    for j in range(boss.col_size+c):
                                        if board[x[0]][x[1]] == boss.board_pos[i][j]:
                                            boss.health -= (abs(B.vx) +
                                                            abs(B.vy))
                                            if boss.health < 0:
                                                boss.health = 0
                                            if boss.health <= boss.crit_health2 and boss.defense2 == True:
                                                boss.engage(
                                                    board, balls, powerups, bombs, bullets, 2)
                                                boss.defense1 = False
                                                boss.defense2 = False
                                            elif boss.health <= boss.crit_health1 and boss.defense1 == True:
                                                boss.engage(
                                                    board, balls, powerups, bombs, bullets, 1)
                                                boss.defense1 = False
                                            break

                        # for ball collision with brick/paddle update ball
                        B.collisions(x, prev_x)
                        B.update_block()
                        if B.through == 0:
                            break
                    prev_x = x

                B.paddle_touch = 0
                if B.x == P.x-1 and B.y >= P.c and B.y < P.c + 5*P.size:
                    B.paddle_touch = 1

                # (ball drops out of map)
                if B.x > 30:
                    balls.remove(B)
                    if len(balls) == 0:
                        P.life = P.life - 1
                        for t in range(len(rem_time)):
                            rem_time[t] = 0
                        for i, pw in enumerate(powerups):
                            pw.delete(pw)
                        # powerups = [pw for pw in powerups if pw.passive != 1]
                        powerups.clear()
                        bombs.clear()
                        bullets.clear()
                        P.grab = 1
                        y = random.randint(P.c, P.c+5*P.size-1)
                        B = Ball(29, y, 2, (y-P.c)//P.size - 2)
                        balls.append(B)
                else:
                    board[B.x][(B.y+4)//5] = B.board_pos

            bricks_rem = 0
            for row in board:
                for b in row:
                    if b == brickcol[1] or b == brickcol[2] or b == brickcol[3]:
                        bricks_rem += 1
            if (bricks_rem == 0 and P.level <= 2) or \
                    (P.level == 3 and boss.health == 0):
                P.level = P.level + 1
                P.play = 0
                P.setup = True

            Print(powerups)
            print('\n')
            
            # print(ali)
            for i, pw in enumerate(powerups):
               pw.update(pw,i)
            powerups = [pw for pw in powerups if pw.passive != 1 ]
            # print(powerups)
            # for pw_index in powerups_del:
            #     # powerups.remove(pw)
            #     powerups.pop(pw_index)
            # powerups_del.clear()

            if P.level == 3:
                print(' BOSS Health: \n [', end='')
                for i in range(100):
                    if i < boss.health:
                        print('#', end='')
                    else:
                        print('-', end='')
                print(']  (', boss.health, '% ) \n')

            pw = Power0(1, 1, 1, 1)
            if rem_time[0] > 0:
                print(pw.board_pos,
                      '\tEXPAND PADDLE\tRemaining time: ', rem_time[0])
            pw = Power1(1, 1, 1, 1)
            if rem_time[1] > 0:
                print(pw.board_pos,
                      '\tSHRINK PADDLE\tRemaining time: ', rem_time[1])
            pw = Power2(1, 1, 1, 1)
            if len(balls) > 1:
                print(pw.board_pos,
                      '\tBALL MULTIPLIER\tRemaining balls: ', len(balls))
            pw = Power3(1, 1, 1, 1)
            if rem_time[3] > 0:
                print(pw.board_pos,
                      '\tFAST BALL\tRemaining time: ', rem_time[3])
            pw = Power4(1, 1, 1, 1)
            if rem_time[4] > 0:
                print(pw.board_pos,
                      '\tTHROUGH BALL\tRemaining time: ', rem_time[4])
            pw = Power5(1, 1, 1, 1)
            if rem_time[5] > 0:
                print(pw.board_pos,
                      '\tPADDLE GRAB\tRemaining time: ', rem_time[5])
            pw = Power6(1, 1, 1, 1)
            if rem_time[6] > 0:
                print(pw.board_pos,
                      '\tSHOOTING PADDLE\tRemaining time: ', rem_time[6])
            pw = Power7(1, 1, 1, 1)
            if rem_time[7] > 0:
                print(pw.board_pos,
                      '\tFIRE BALL\tRemaining time: ', rem_time[7])

            if P.play == 0:
                time.sleep(2)
            # print(colors.bg.yellow,colors.fg.red,board[B.x][(B.y+4)//5],colors.reset,'  ',B.x,'  ',B.y)
            # if rem_time[2] > 0:
            #     print(t0)
            # print(colors.bg.yellow,colors.fg.red,B.board_pos,colors.reset,' ',B.vx,' ',B.vy)
            # print(type(r_bricks[0]),' ')
            # print(powerups_del,' ')

        if P.life == 0 or P.level == 4:
            print('\n\n\t\t\t┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼\n',
                  '\t\t\t███▀▀▀██┼███▀▀▀███┼███▀█▄█▀███┼██▀▀▀\n',
                  '\t\t\t██┼┼┼┼██┼██┼┼┼┼┼██┼██┼┼┼█┼┼┼██┼██┼┼┼\n',
                  '\t\t\t██┼┼┼▄▄▄┼██▄▄▄▄▄██┼██┼┼┼▀┼┼┼██┼██▀▀▀\n',
                  '\t\t\t██┼┼┼┼██┼██┼┼┼┼┼██┼██┼┼┼┼┼┼┼██┼██┼┼┼\n',
                  '\t\t\t███▄▄▄██┼██┼┼┼┼┼██┼██┼┼┼┼┼┼┼██┼██▄▄▄\n',
                  '\t\t\t┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼\n',
                  '\t\t\t███▀▀▀███┼▀███┼┼██▀┼██▀▀▀┼██▀▀▀▀██▄┼\n',
                  '\t\t\t██┼┼┼┼┼██┼┼┼██┼┼██┼┼██┼┼┼┼██┼┼┼┼┼██┼\n',
                  '\t\t\t██┼┼┼┼┼██┼┼┼██┼┼██┼┼██▀▀▀┼██▄▄▄▄▄▀▀┼\n',
                  '\t\t\t██┼┼┼┼┼██┼┼┼██┼┼█▀┼┼██┼┼┼┼██┼┼┼┼┼██┼\n',
                  '\t\t\t███▄▄▄███┼┼┼─▀█▀┼┼─┼██▄▄▄┼██┼┼┼┼┼██▄\n',
                  '\t\t\t┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼\n',
                  '\t\t\t┼┼┼┼┼┼┼┼██┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼██┼┼┼┼┼┼┼┼┼\n',
                  '\t\t\t┼┼┼┼┼┼████▄┼┼┼▄▄▄▄▄▄▄┼┼┼▄████┼┼┼┼┼┼┼\n',
                  '\t\t\t┼┼┼┼┼┼┼┼┼▀▀█▄█████████▄█▀▀┼┼┼┼┼┼┼┼┼┼\n',
                  '\t\t\t┼┼┼┼┼┼┼┼┼┼┼█████████████┼┼┼┼┼┼┼┼┼┼┼┼\n',
                  '\t\t\t┼┼┼┼┼┼┼┼┼┼┼██▀▀▀███▀▀▀██┼┼┼┼┼┼┼┼┼┼┼┼\n',
                  '\t\t\t┼┼┼┼┼┼┼┼┼┼┼██┼┼┼███┼┼┼██┼┼┼┼┼┼┼┼┼┼┼┼\n',
                  '\t\t\t┼┼┼┼┼┼┼┼┼┼┼█████▀▄▀█████┼┼┼┼┼┼┼┼┼┼┼┼\n',
                  '\t\t\t┼┼┼┼┼┼┼┼┼┼┼┼███████████┼┼┼┼┼┼┼┼┼┼┼┼┼\n',
                  '\t\t\t┼┼┼┼┼┼┼┼▄▄▄██┼┼█▀█▀█┼┼██▄▄▄┼┼┼┼┼┼┼┼┼\n',
                  '\t\t\t┼┼┼┼┼┼┼┼▀▀██┼┼┼┼┼┼┼┼┼┼┼██▀▀┼┼┼┼┼┼┼┼┼\n',
                  '\t\t\t┼┼┼┼┼┼┼┼┼┼▀▀┼┼┼┼┼┼┼┼┼┼┼▀▀┼┼┼┼┼┼┼┼┼┼┼\n',
                  '\t\t\t┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼\n')
            print('\n\t\t\tYour Score = ', P.score, end='\n\n')
            if P.level <= 3:
                print('\n\t\t\tHighest Level = ', P.level, end='\n\n')
            else:
                print('\n\t\t\tAll Levels cleared !!!', end='\n\n')
            break

        elif P.level == 2 and P.setup == True:
            balls.clear()
            for t in range(len(rem_time)):
                rem_time[t] = 0
            for i, pw in enumerate(powerups):
                pw.delete(pw)
            # powerups = [pw for pw in powerups if pw.passive != 1]
            powerups.clear()
            bombs.clear()
            bullets.clear()
            P.grab = 1
            y = random.randint(P.c, P.c+5*P.size-1)
            B = Ball(29, y, 1, (y-P.c)//P.size - 2)
            balls.append(B)
            setup2(board)
            P.setup = False
            Print(powerups)

        elif P.level == 3 and P.setup == True:
            balls.clear()
            for t in range(len(rem_time)):
                rem_time[t] = 0
            for i, pw in enumerate(powerups):
                pw.delete(pw)
            # powerups = [pw for pw in powerups if pw.passive != 1]
            powerups.clear()
            bombs.clear()
            bullets.clear()
            P.grab = 1
            y = random.randint(P.c, P.c+5*P.size-1)
            B = Ball(29, y, 1, (y-P.c)//P.size - 2)
            balls.append(B)
            setup3(board, ufo)
            P.setup = False
            Print(powerups)

        if isData():
            inp = sys.stdin.read(1)

            if inp == 'q':
                break
            if inp == 'p':
                P.play = 1 - P.play
                Print(powerups)
            if inp == 'n' and P.level <= 2:
                # increase 1 level
                balls.clear()
                for t in range(len(rem_time)):
                    rem_time[t] = 0
                for i, pw in enumerate(powerups):
                    pw.delete(pw)
                # powerups = [pw for pw in powerups if pw.passive != 1]
                powerups.clear()
                bombs.clear()
                bullets.clear()
                P.grab = 1
                y = random.randint(P.c, P.c+5*P.size-1)
                B = Ball(29, y, 1, (y-P.c)//P.size - 2)
                balls.append(B)
                if P.level == 1:
                    setup2(board)
                elif P.level == 2:
                    setup3(board, ufo)
                P.level += 1
                P.setup = False
                Print(powerups)
            if inp == 'm' and P.level >= 2:
                # decrease 1 level
                balls.clear()
                for t in range(len(rem_time)):
                    rem_time[t] = 0
                for i, pw in enumerate(powerups):
                    pw.delete(pw)
                # powerups = [pw for pw in powerups if pw.passive != 1]
                powerups.clear()
                bombs.clear()
                bullets.clear()
                P.grab = 1
                y = random.randint(P.c, P.c+5*P.size-1)
                B = Ball(29, y, 1, (y-P.c)//P.size - 2)
                balls.append(B)
                if P.level == 3:
                    setup2(board)
                elif P.level == 2:
                    setup1(board)
                P.level -= 1
                P.setup = False
                Print(powerups)

            if P.play:
                if inp == 'a' and P.c > 1:
                    if P.grab:
                        for B in balls:
                            if B.paddle_touch:
                                board[B.x][(B.y+4)//5] = brickcol[0]
                                B.left()
                                board[B.x][(B.y+4)//5] = B.board_pos

                    for cnt in range(0, P.size+1):
                        board[P.x][P.y+cnt] = brickcol[0]

                    if P.level == 3 and P.y > 3 and P.y < 16:
                        for i in range(boss.row_size):
                            for j in range(boss.col_size+1):
                                board[boss.x+i][boss.y+j] = brickcol[0]
                        boss.left(ufo)
                        for i in range(boss.row_size):
                            for j in range(boss.col_size+1):
                                board[boss.x+i][boss.y +
                                                j] = boss.board_pos[i][j]

                    P.left()
                    for cnt in range(0, P.size+1):
                        board[P.x][P.y+cnt] = P.board_pos[cnt]
                    Print(powerups)

                if inp == 'd' and P.c <= 100 - 5*P.size:
                    if P.grab:
                        for B in balls:
                            if B.paddle_touch:
                                board[B.x][(B.y+4)//5] = brickcol[0]
                                B.right()
                                board[B.x][(B.y+4)//5] = B.board_pos
                    for cnt in range(0, P.size+1):
                        board[P.x][P.y+cnt] = brickcol[0]

                    if P.level == 3 and P.y > 3 and P.y < 16:
                        for i in range(boss.row_size):
                            for j in range(boss.col_size+1):
                                board[boss.x+i][boss.y+j] = brickcol[0]
                        boss.right(ufo)
                        for i in range(boss.row_size):
                            for j in range(boss.col_size+1):
                                board[boss.x+i][boss.y +
                                                j] = boss.board_pos[i][j]

                    P.right()
                    for cnt in range(0, P.size+1):
                        board[P.x][P.y+cnt] = P.board_pos[cnt]
                    Print(powerups)

                if inp == ' ':
                    P.grab = 0
                if inp == '*':
                    P.grab = 1
finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
