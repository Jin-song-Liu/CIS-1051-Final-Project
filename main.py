import pygame
import sys
import time
import random
from pygame.math import Vector2


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

        self.snake_head_up = pygame.image.load("pictures/snakeup.png").convert_alpha()
        self.snake_head_down = pygame.image.load("pictures/snakedown.png").convert_alpha()
        self.snake_head_left = pygame.image.load("pictures/snakeleft.png").convert_alpha()
        self.snake_head_right = pygame.image.load("pictures/snakeright.png").convert_alpha()

        self.snake_tail_up = pygame.image.load("pictures/tailup.png").convert_alpha()
        self.snake_tail_down = pygame.image.load("pictures/taildown.png").convert_alpha()
        self.snake_tail_left = pygame.image.load("pictures/tailleft.png").convert_alpha()
        self.snake_tail_right = pygame.image.load("pictures/tailright.png").convert_alpha()

    def drawSnake(self):
        self.snake_head_direction()
        self.snake_tail_direction()

        for index, block in enumerate(self.body):
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            snake_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                game_screen_resolution.blit(self.head, snake_rect)

            elif index == len(self.body) - 1:

                game_screen_resolution.blit(self.tail, snake_rect)

            else:
                pygame.draw.rect(game_screen_resolution, blue, snake_rect)
    
    def snake_head_direction(self):
        head_direction = self.body[1] - self.body[0]
        if head_direction == Vector2(1,0):
            self.head = self.snake_head_left
        elif head_direction == Vector2(-1,0):
            self.head = self.snake_head_right
        elif head_direction == Vector2(0,1):
            self.head = self.snake_head_up
        elif head_direction == Vector2(0,-1):
            self.head = self.snake_head_down

    def snake_tail_direction(self):
        tail_direction = self.body[-2] - self.body[-1]
        if tail_direction == Vector2(1,0):
            self.tail = self.snake_tail_left
        elif tail_direction == Vector2(-1,0):
            self.tail = self.snake_tail_right
        elif tail_direction == Vector2(0,1):
            self.tail = self.snake_tail_up
        elif tail_direction == Vector2(0,-1):
            self.tail = self.snake_tail_down



    def moveSnake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def addBlock(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)


class FOOD:
    def __init__(self):
        self.randomize()

    def drawFood(self):
        x_pos = self.pos.x * cell_size
        y_pos = self.pos.y * cell_size
        food_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        game_screen_resolution.blit(rat, food_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class OBSTACLES:

    def __init__(self):
        x_pos = random.randint(0, cell_number -1)
        y_pos =random.randint(0, cell_number -1)
        obstacle_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.food = FOOD()
        self.obstacles = OBSTACLES()

    def update(self):
        self.snake.moveSnake()
        self.checkCollision()
        self.checkSelfCollision()

    def drawElements(self):
        self.food.drawFood()
        self.snake.drawSnake()
        self.scoreBoard()

    def checkCollision(self):
        if self.food.pos == self.snake.body[0]:
            self.food.randomize()
            self.snake.addBlock()


    def checkSelfCollision(self):
        if not 0 <= self.snake.body[0].x < cell_number:
            self.gameOver()
        if not 0 <= self.snake.body[0].y < cell_number:
            self.gameOver()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameOver()

    def gameOver(self):
        self.snake.reset()

    def scoreBoard(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, red)
        score_x_postion = int(cell_number * cell_size - 100)
        score_y_position = int(cell_number * cell_size - 100)
        score_rect = score_surface.get_rect(center = (score_x_postion, score_y_position))
        rat_rect = rat.get_rect(midright = (score_rect.left, score_rect.centery))
        back_ground = pygame.Rect(rat_rect.left, rat_rect.top, rat_rect.width + score_rect.width , rat_rect.height)
        pygame.draw.rect(game_screen_resolution, (black), back_ground)
        game_screen_resolution.blit(score_surface, score_rect)  
        game_screen_resolution.blit(rat, rat_rect)
        
        


pygame.init()
cell_size = 40
cell_number = 20
game_screen_resolution = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
clock = pygame.time.Clock()
rat = pygame.image.load("pictures/rat.png").convert_alpha()
game_font = pygame.font.Font(None, 50)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)

    game_screen_resolution.fill(white)
    main_game.drawElements()
    pygame.display.update()
    clock.tick(60)


