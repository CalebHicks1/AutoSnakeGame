import pygame
import random
import threading
import time
import copy

# ~ Initialize Variables --------------------------------------------------------

width = 300
height = 300
game_over = False
MAKESNAKE = pygame.USEREVENT + 1
timer = pygame.time.set_timer(MAKESNAKE, 150)
x_pos = width // 2
y_pos = height // 2
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
direction = 'U'
body_x = []
body_y = []
body_pos = []
growing = True
grow_time = 0
apple_x = 0
apple_y = 0
apple_found = False
directions = []
tl = threading.local()

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
    if [apple_x,apple_y] == [x_pos,y_pos]:
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
    if [x_pos,y_pos] in body_pos:
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
    move()
    body_x.append(x_pos)
    body_y.append(y_pos)
    body_pos.append([x_pos, y_pos])
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
    global apple_found
    apple_found = False
    global apple_x
    global apple_y
    apple_x = random.randint(1, (width-30) // 30)
    apple_y = random.randint(1,(height-30) // 30)
    apple_x *= 30
    apple_y *= 30
    if [apple_x,apple_y] in body_pos:
        move_apple()
        return
    pygame.draw.rect(dis, red, [apple_x, apple_y,25,25])
    print(apple_x,apple_y)

def start_thread(dir, color, prev_moves, dir_list, curr_x, curr_y):
    thread = threading.Thread(target=thread_action, args=(dir, prev_moves, dir_list, curr_x, curr_y, color))
    thread.start()

def start_threads(thread_color, prev_moves, dir_list, curr_x, curr_y):
    if apple_found:
        return

    tl.moves = copy.deepcopy(prev_moves)
    u_thread = threading.Thread(target=thread_action, args=('U', tl.moves, dir_list, curr_x, curr_y, thread_color))

    d_thread = threading.Thread(target=thread_action, args=('D', tl.moves, dir_list, curr_x, curr_y, thread_color))

    r_thread = threading.Thread(target=thread_action, args=('R', tl.moves, dir_list, curr_x, curr_y, thread_color))

    l_thread = threading.Thread(target=thread_action, args=('L', tl.moves, dir_list, curr_x, curr_y, thread_color))

    u_thread.start()
    d_thread.start()
    r_thread.start()
    l_thread.start()

def thread_action(dir, prev_moves, dir_list, curr_x, curr_y, color):
    global apple_found
    global directions
    if apple_found:
        return
    if dir == 'U':
        new_move = [curr_x, curr_y-30]
    elif dir == 'D':
        new_move = [curr_x, curr_y+30]
    elif dir == 'R':
        new_move = [curr_x+30, curr_y]
    elif dir == 'L':
        new_move = [curr_x-30, curr_y]
    if new_move in prev_moves:
        return
    elif new_move[0] > width - 30 or new_move[0] < 0:
        return
    elif new_move[1] > height -30 or new_move[1] < 0:
        return
    elif [curr_x, curr_y] == [apple_x, apple_y]:
        apple_found = True
        tl.move_list = copy.deepcopy(dir_list)
        tl.move_list.append(dir)
        directions = tl.move_list
        pygame.draw.rect(dis, green, [curr_x, curr_y, 25, 25])
        pygame.display.update()
        return
    else:
        tl.moves = copy.deepcopy(prev_moves)
        tl.moves.append(new_move)
        tl.move_list = copy.deepcopy(dir_list)
        tl.move_list.append(dir)
        pygame.draw.rect(dis, color, [curr_x, curr_y, 25, 25])
        pygame.display.update()
        #if len(tl.moves) > 55:
        #    return
        start_threads(color, tl.moves, tl.move_list, new_move[0], new_move[1])

# ~ Gameplay Loop ------------------------------------------------------

move_apple()
pygame.display.update()
time.sleep(0.7)
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == MAKESNAKE:
            if apple_found:
                if directions:
                    direction = directions.pop(0)
                    time.sleep(0.25)
                    make_snake()
            else:
                thread_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                direction_list = ['U','D','R','L']
                for i in direction_list:
                    if i == direction:
                        continue
                    start_thread(i,thread_color, body_pos, [], x_pos, y_pos)
                while not apple_found:
                    time.sleep(0.1)
                    if game_over:
                        break
        pygame.display.update()
pygame.quit()
quit()

"""
TODO LIST ----------------------
1. make threads account for movement of snake.
    maybe pop body off as each new thread is made

"""
