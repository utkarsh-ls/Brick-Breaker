# Brick Breaker Game
# README 
* ## by UTKARSH UPADHYAY
* ## Roll No. 2019101010
---
---

## About
This is an arcade game in Python3 (terminal-based), inspired from the old classic brick breaker similar to this. The player will be using a paddle with a bouncing ball to smash a wall of bricks and make high scores! The objective of the game is to break all the bricks as fast as possible and beat the highest score! You lose a life when the ball touches the ground below the paddle.
The game design is done using OOPS concepts.

## How to run
Open the project directory and run the following command:
```c
python3 game.py
```

## Startup
Initially, the ball would appear randomly on top of the paddle at any point.

## Movement keys
```c
a   => Move left
d   => Move right
' ' => Paddle releases ball
q   => Quit game
p   => Toggle pause/continue game
n   => Increase level
m   => Decrease level
```
## Collision Handling
All the collisions are elastic as follows:
1) Ball/bullet and bricks:
* Handle collisions with four sides of the brick and corners (see assumptions).
* Each time a collision happens, the strength of brick decreases by one unit (except for
unbreakable bricks) and when the strength becomes zero, the brick disappears.
2) Ball and paddle:
* Handle collisions with only the top face of the paddle (side collisions are there but they don't matter as the ball will go below the paddle irrescpective of the collsion).
* The direction of movement of the ball after collision with the paddle will depend on the distance from the center of the paddle and the collision point, i.e further the ball hits from the center, more the deflection.
* Collision on left side of paddle imparts velocity in left direction and vice versa.
3) Ball/powerups and wall:
* Handle collisions with 3 sides of the walls (except the bottom one).
* The reflections should be based on the side the ball hits the wall.
* The ball is lost when it hits the bottom wall (missing the paddle).
4) Ball and boss:
* Handle perfect inelastic collisions with 3 sides of the boss boundaries (except the top one).
* Each time a ball hits boss, boss loses life proportional to speed of the ball.
5) Bomb and paddle:
* Handle collisions with only the top face of the paddle.
* If bomb hits the paddle, it loses a life.

## Bricks
* Different colored bricks , with their color indicating their strength The strength of bricks is written on them.
* Bricks with more strength require more number of hits to make them disappear.
* Strength of the breakable bricks: Red (1 hit) < Green (2 hits) < Blue (3 hits)
* With decrease in strength of a brick due to hits from the ball, the color of the brick changes
accordingly.
* Also there are Unbreakable bricks (purple bricks) which cannot be broken by the ball.
* Then there are Rainbow bricks (initially white bricks) which changes color continously until first hit by a ball.

## Levels
* Game contains 3 levels.
* For clearing first 2 levels, you just need to clear all the bricks.
* For clearing the last (boss) level, you need to decrease the boss helath to 0.

## Score and Time
* Display Score, Lives remaining and Time played on the screen. 
* A life is lost when all the balls in the game are lost (touches the ground below the paddle).

## Power-Ups
Each of these power-ups are appear randomly as catchable objects on destroying a brick.
The power-ups have the velocity of the ball that hit them when they spawn.
All power-ups are are present only for a fixed amount of time (except ball multiplier).
1. Expand Paddle: Increases the size of the paddle by a certain amount.
2. Shrink Paddle: Reduce the size of the paddle by a certain amount but not completely.
3. Ball Multiplier: Each of the balls which are present will be further divided into two debug needed.
4. Fast Ball: Increases the speed of the ball.
5. Thru-ball: This enables the ball to destroy and go through any brick it touches, irrespective of the strength of the wall (even the unbreakable ones which you couldn’t previously destroy).
6. Paddle Grab: Allows the paddle to grab the ball on contact and relaunch the ball at will. The ball will follow the same expected trajectory after release, similar to the movement expected without the grab.
7. Shooting paddle: This power-up will enable the paddle to shoot bullets in order to break the bricks. The strength of each of these bullets is same as the ball.
8. Fire-Ball: This powerup is similar to the exploding bricks powerup except the same effect is caused by the ball on hitting the bricks.

## Boss
* The final level of the game will have the boss enemy along with a few unbreakable bricks.
* The boss enemy is a UFO which flies at the top of the screen and follows the paddle (moves along with it).
* The UFO drops bombs in regular intervals onto the paddle (which travel linearly downwards), on being hit by these bombs the paddle loses one life.
* The UFO has a health which reduces on hitting it directly will a ball (health bar is shown as well). The collisions with the UFO are similar to the other collisions that we have
 implemented before.
* The UFO will be able to spawn defensive bricks around it(not unbreakable ones) after it’s health falls below a certain range. The defensive strategy would be an entire layer below
 the UFO and it can use this twice. These bricks will form a layer under the UFO and breaking of these bricks would not yield a power-up.

## Bonus
1. The bonus part includes exploding bricks (yellow color) which explodes the bricks around them (horizontally, vertically and diagonally) when a ball collides with them.
2. For assignment 2, the bonus includes the fireball powerup and adding sound effects in the game events.

## Assumptions
* Ball is considered a point object, while the paddle and bricks are rectangles, and their collisions are handled accordingly.
* Ball can collide with the corner of paddle/brick in which case it retraces it's incoming path.
* Ball muliplier powerup has infinite timer (i.e., the ball will remain on the board as long as the player doesn't let it go below the paddle).
* Through Ball is applied only to existing balls, if new balls are spawned using mulitplier they don't have this powerup.
* Maximum powerups allowed at a time are 4.