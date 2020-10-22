import pygame
import random

# ~ Initialize --------------------------------------------------------

width = 600
height = 600
game_over = False
MAKESNAKE = pygame.USEREVENT + 1
timer = pygame.time.set_timer(MAKESNAKE, 100)
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

def solve():
    print('solve()')
    global direction
    global apple_x
    global apple_y
    global x_pos
    global y_pos
    # Setup variables to locate apple.
    x_dir_to_apple = 'R'
    y_dir_to_apple = 'U'
    if apple_x > x_pos:
        x_dir_to_apple = 'R'
    else:
        x_dir_to_apple = 'L'
    if apple_y > y_pos:
        y_dir_to_apple = 'D'
    else:
        y_dir_to_apple = 'U'
    if direction != x_dir_to_apple or direction != y_dir_to_apple or going_off_edge():
        change_direction()

def change_direction():
    print('change_direction()')
    global direction
    global apple_x
    global apple_y
    global x_pos
    global y_pos
    if x_pos > apple_x:
        if direction != 'R':
            print("direction: L")
            direction = 'L'
        else:
            print("direction: U")
            direction = 'U'
    elif x_pos < apple_x:
        if direction != 'L':
            print("direction: R")
            direction = 'R'
        else:
            print("direction: U")
            direction = 'U'
    elif y_pos > apple_y:
        if direction != 'D':
            print("direction: U")
            direction = 'U'
        else:
            print("direction: R")
            direction = 'R'
    elif y_pos < apple_y:
        if direction != 'U':
            print("direction: D")
            direction = 'D'
        else:
            print("direction: R")
            direction = 'R'
    direction = clear()

def going_off_edge():
    print("going_off_edge()")
    if direction == 'U':
        if y_pos - 30 == 0:
            return True
    if direction == 'D':
        if y_pos + 30 == height:
            return True
    if direction == 'R':
        if x_pos + 30 == width:
            return True
    if direction == 'U':
        if x_pos - 30 == 0:
            return True

"""
tells if the space in front of snake is clear.
If not, it checks the two perpendicular directions.
"""
def clear():
    print('clear()')
    if direction == 'U':
        if '%d,%d' % (x_pos, y_pos - 30) not in body_pos and y_pos -30 > 0:
            return direction
        else:
            if '%d,%d' % (x_pos + 30, y_pos) not in body_pos:
                return 'R'
            else:
                return 'L'
    if direction == 'D':
        if '%d,%d' % (x_pos, y_pos + 30) not in body_pos and y_pos +30 < height:
            return direction
        else:
            if '%d,%d' % (x_pos + 30, y_pos) not in body_pos:
                return 'R'
            else:
                return 'L'
    if direction == 'R':
        if '%d,%d' % (x_pos + 30, y_pos) not in body_pos:
            return direction
        else:
            if '%d,%d' % (x_pos, y_pos + 30) not in body_pos:
                return 'D'
            else:
                return 'U'
    if direction == 'L':
        if '%d,%d' % (x_pos - 30, y_pos) not in body_pos and x_pos - 30 > 0:
            return direction
        else:
            if '%d,%d' % (x_pos, y_pos + 30) not in body_pos and x_pos + 30 < width:
                return 'D'
            else:
                return 'U'


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
            solve()
        pygame.display.update()
pygame.quit()
quit()
