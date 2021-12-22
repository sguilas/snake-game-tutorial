import pygame
import sys
import random
from pygame.math import Vector2 # Use Vectors to find relation between each rectangle drawn on screen


class FRUIT:
    def __init__(self): # constructor to create fruit object
        self.randomize()

    def draw_fruit(self): # draws the fruit object
        fruit_rect=pygame.Rect(int(self.pos.x*cell_size), int(self.pos.y*cell_size), cell_size, cell_size) # creates a rectangle needs ( position x,y and lenght and width
        screen.blit(apple,fruit_rect) # screen.blit draws the png over the rect
        ## Ran into problem where the png was too big. Had to resize using online tool and change cell size to fit
        #pygame.draw.rect(screen, (126,166,114), fruit_rect)  # draws the rectangle (where to draw, color, which rectangle)
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)  # randomizes the position with each instance
        self.y = random.randint(0, cell_number - 1)  # after the fruit been eaten
        self.pos = Vector2(self.x, self.y)

class SNAKE:
    def __init__(self):
        self.body=[Vector2(5,10),Vector2(4,10),Vector2(3,10)] # creating body. Positions of blocks on screen
        self.direction=Vector2(1,0)
        self.new_block= False  # not making it longer by default

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            snake_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            if index==0: # index = 0 is the head
                screen.blit(self.head,snake_rect)  # forgot parentheses so code wouldn't work. found and fixed.
            elif index == len(self.body)-1: # index = lenght -1 is the tail
                screen.blit(self.tail,snake_rect)
            else:
                prev_block = self.body[index+1] - block
                next_block = self.body[index-1] - block
                if prev_block.x == next_block.x:
                    screen.blit(self.body_vertical,snake_rect)
                elif prev_block.y == next_block.y:
                    screen.blit(self.body_horizontal,snake_rect)
                else:
                    if prev_block.x == -1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,snake_rect)
                    elif prev_block.x == -1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,snake_rect)
                    elif prev_block.x == 1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,snake_rect)
                    elif prev_block.x == 1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,snake_rect)

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]  # Use vectors to find relation of last and second to last block
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def update_head_graphics(self):  # Use vectors to find relation of first and second block
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0):
            self.head = self.head_left
        elif head_relation == Vector2(-1,0):
            self.head = self.head_right
        elif head_relation == Vector2(0,1):
            self.head = self.head_up
        elif head_relation == Vector2(0,-1):
            self.head = self.head_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]  #copy the whole snake and add a head (snake lenght + head)
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block=False
        else:
            body_copy = self.body[:-1] # copy only a part of the snake and add a head (snake lenght -1 + head)
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

class MAIN():  # This main class will contain everything about the game
    def __init__(self):
        self.snake = SNAKE()  # creates the new object using snake class
        self.fruit = FRUIT()  # creates the fruit

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()  # see in game
        self.snake.draw_snake()  # see in game

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:  # if the snake head is the same position as the fruit
            self.fruit.randomize()  # reposition fruit after eaten
            self.snake.add_block()  # make snake longer
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    def game_over(self):
        pygame.quit()
        sys.exit()

    def draw_grass(self):
        grass_color = (34,139,34)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col%2 ==0:
                        grass_rect = pygame.Rect(col * cell_size, row* cell_size, cell_size,cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col%2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row* cell_size, cell_size,cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

pygame.init()
cell_size=40
cell_number=20
screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/orange2.png').convert_alpha()  # loads an image from a folder. Only works if code is in same folder as graphics folder

main_game=MAIN()

SCREEN_UPDATE=pygame.USEREVENT  # updates the screen so that the snake looks like its moving
pygame.time.set_timer(SCREEN_UPDATE,100)  # timer to trigger event (SCREEN_UPDATE in this instance)
                                          # needs event and the time (150 this is in milliseconds)
while True:  # The event loop               # How fast the snake moves (more=slower)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:  # keyboard inputs
            if event.key == pygame.K_UP: # K_UP corresponds to the up key
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)  # when up key is pushed snake moves up
            elif event.key == pygame.K_DOWN:  # K_DOWN corresponds to the down key
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)  # when down key is pushed snake moves down
            elif event.key == pygame.K_RIGHT:  # K_RIGHT corresponds to the right key
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)  # when right key is pushed snake moves right
            elif event.key == pygame.K_LEFT:  # K_LEFT corresponds to the left key
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)  # when left key is pushed snake moves left
    screen.fill((0, 128, 0))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)