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
            self.direction = DIRECTION.RIGHT
            self.score = 0
            self.head = Point(self.width // 2, self.height // 2)
            self.snake = self.head
            self.food = None
            self.place_food()
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
            self.snake.inser(0, self.head)

            if self.is_collision():
                gameover = True
                reward -= 10
                return reward,gameover, self.score

        def is_collision(pt):
            """
            checkss if snake has collided with itself or with the boundaries
            """
            if pt.x < 0 or pt.x >= self.width or pt.y < 0 or pt.y >= self.height:
                return True
            if pt.x in self.snake[1:]:
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

        def render():
            """
            renders the game window using pygame
            """
