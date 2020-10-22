import pygame
import random

# ~ Initialize --------------------------------------------------------

width = 600
height = 600
game_over = False
MAKESNAKE = pygame.USEREVENT + 1
timer = pygame.time.set_timer(MAKESNAKE, 250)
x_pos = width // 2
y_pos = height // 2
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
direction = 'U'
body_x = []
body_y = []
body_pos = []
growing = True
grow_time = 0
apple_x = 0
apple_y = 0

pygame.init()
dis = pygame.display.set_mode((width,height))
pygame.display.set_caption('Snake Game by Caleb')
pygame.display.update()

# ~ Helper Functions ---------------------------------------------------

"""
removes piece in snake body specified by x,y
"""
def remove_tail(x : int, y : int):
    pygame.draw.rect(dis, black, [x,y,30,30])

"""
moves snake head based on direction variable. sets game_over
to true if snake collides with itself or with walls
"""
def move():
    global game_over
    global width
    global height
    global x_pos
    global y_pos
    global grow_time
    if '%d,%d'%(apple_x,apple_y) == '%d,%d'%(x_pos,y_pos):
        move_apple()
        grow_time = 0
    if direction == 'U':
        y_pos -= 30
    elif direction == 'D':
        y_pos += 30
    elif direction == 'R':
        x_pos += 30
    elif direction == 'L':
        x_pos -= 30
    if x_pos < 0 or x_pos >= width:
        game_over = True
    elif y_pos < 0 or y_pos >= height:
        game_over = True
    if '%d,%d'%(x_pos,y_pos) in body_pos:
        game_over = True
        print('collide')

"""
draws new snake section. If snake is growing, doesn't call
remove_tail
"""
def make_snake():
    global grow_time
    global growing
    if not growing:
        remove_tail(body_x.pop(0), body_y.pop(0))
        body_pos.pop(0)
    if direction == 'U':
        pygame.draw.rect(dis, white, [x_pos, y_pos-5, 25, 30]) 
    elif direction == 'D':
        pygame.draw.rect(dis, white, [x_pos, y_pos, 25, 30])
    elif direction == 'R':
        pygame.draw.rect(dis, white, [x_pos, y_pos, 30, 25])
    elif direction == 'L':
        pygame.draw.rect(dis, white, [x_pos-5, y_pos, 30, 25])
    body_x.append(x_pos)
    body_y.append(y_pos)
    body_pos.append('%d,%d' % (x_pos, y_pos))
    move()
    if grow_time < 5:
        growing = True
        grow_time += 1
    else:
        growing = False

"""
moves the apple to a random place on the screen.
position is a multiple of 30 so that it is in the same grid as the snake
"""
def move_apple():
    global apple_x
    global apple_y
    apple_x = random.randint(1, (width-30) // 30)
    apple_y = random.randint(1,(height-30) // 30)
    apple_x *= 30
    apple_y *= 30
    if '%d,%d'%(apple_x,apple_y) in body_pos:
        move_apple()
        return
    pygame.draw.rect(dis, red, [apple_x, apple_y,25,25])
    print(apple_x,apple_y)

# ~ Gameplay Loop ------------------------------------------------------

move_apple()
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != 'R':
                direction = 'L'
            elif event.key == pygame.K_RIGHT and direction != 'L':
                direction = 'R'
            elif event.key == pygame.K_DOWN and direction != 'U':
                direction = 'D'
            elif event.key == pygame.K_UP and direction != 'D':
                direction = 'U'
            elif event.key == pygame.K_SPACE:
                grow_time = 0
        if event.type == MAKESNAKE:
            make_snake()
        pygame.display.update()
pygame.quit()
quit()
