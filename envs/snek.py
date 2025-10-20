import pygame
import random
import numpy as np
from enum import Enum
from collections import namedtuple

Point = namedtuple('Point', 'x,y')
BLOCK_SIZE = 20

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class snekEnv:

    def __init__(self,width = 640, height = 480):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
            """
            resets the snake game to initial state
            snake moving to the right
            middle of the screen
            score is 0
            """
            self.direction = Direction.RIGHT
            self.score = 0
            self.head = Point(self.width // 2, self.height // 2)
            self.snake = [self.head]
            self.food = None
            self.place_food()
            self.frame = 0
            return np.array([0])
            """ place holder for now it'll return the game state in an array """

    def play_step(self, action):
            """
            increase the frame iteration by 1
            checks for collision
            checks if food was eaten, updates the score
            returns values score, reward and game over (boolean value true or false)
            """
            self.frame += 1
            reward = 0
            gameover = False

            self.move(action)
            self.snake.insert(0, self.head)

            if self.is_collision():
                gameover = True
                reward -= 10
                return reward,gameover, self.score

            if self.head == self.food:
                self.score += 1
                reward += 10
                self.place_food()
            else:
                self.snake.pop()

            return np.array([0]), self.score, reward, gameover

    def move(self,action):
        clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clockwise.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_dir = clockwise[idx]
        elif np.array_equal(action, [0,1,0]):
            new_dir = clockwise[(idx+1)%4]
        else: # [0,0,1] left turn
            new_dir = clockwise[(idx-1)%4]
        self.direction = new_dir

        x,y = self.head
        if self.direction == Direction.RIGHT:
            x+=BLOCK_SIZE
        if self.direction == Direction.LEFT:
            x-=BLOCK_SIZE
        if self.direction == Direction.UP:
            y-=BLOCK_SIZE
        if self.direction == Direction.DOWN:
            y+=BLOCK_SIZE

        self.head = Point(x,y)


    def is_collision(self, pt=None):
            """
            checkss if snake has collided with itself or with the boundaries
            """
            if pt is None:
                pt = self.head
            if pt.x < 0 or pt.x >= self.width or pt.y < 0 or pt.y >= self.height:
                return True
            if pt in self.snake[1:]:
                return True
            return False

    def place_food(self):
            """
            places food on the screen
            if food is on snake body moves it elsewhere
            """
            food_x = random.randint(0, (self.width // BLOCK_SIZE)) * BLOCK_SIZE
            food_y = random.randint(0, (self.height// BLOCK_SIZE)) * BLOCK_SIZE
            self.food = Point(food_x, food_y)
            if self.food in self.snake:
                self.place_food()

    def render(self, screen):
            """
            renders the game window using pygame
            """
            screen.fill((0,0,0))

            #drawing the snek
            for pt in self.snake:
                pygame.draw.rect(screen, (0,255,0), pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))

            #drawing food
            pygame.draw.rect(screen , (255,0,0), pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

            pygame.display.flip()

    if __name__ == "__main__":
        pygame.init()
        env = snekEnv()
        screen = pygame.display.set_mode((env.width, env.height))
        clock = pygame.time.Clock()

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            # simple test action
            action = [1, 0, 0]  # always straight for now
            next_state, score, reward, done = env.play_step(action)

            env.render(screen)
            clock.tick(10)

        pygame.quit()