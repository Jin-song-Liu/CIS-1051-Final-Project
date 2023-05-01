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

    def drawSnake(self):
        for block in self.body:
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            snake_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(game_screen_resolution, green, snake_rect)

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

class FOOD:
    def __init__(self):
        self.randomize()

    def drawFruit(self):
        x_pos = self.pos.x * cell_size
        y_pos = self.pos.y * cell_size
        fruit_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        game_screen_resolution.blit(rat, fruit_rect)
        #pygame.draw.rect(game_screen_resolution, red ,fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.food = FOOD()

    def update(self):
        self.snake.moveSnake()
        self.checkCollision()
        self.checkFail()

    def drawElements(self):
        self.food.drawFruit()
        self.snake.drawSnake()

    def checkCollision(self):
        if self.food.pos == self.snake.body[0]:
            self.food.randomize()
            self.snake.addBlock()

    def checkFail(self):
        if not 0 <= self.snake.body[0].x < cell_number:
            self.gameOver()
        if not 0 <= self.snake.body[0].y < cell_number:
            self.gameOver()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameOver()

    def gameOver(self):
        pygame.quit()
        sys.exit()
        


pygame.init()
cell_size = 40
cell_number = 20
game_screen_resolution = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
clock = pygame.time.Clock()
rat = pygame.image.load("pictures/rat.png").convert_alpha()

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


