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

        def play_step(self, action):
            """
            increase the frame iteration by 1
            checks for collision
            checks if food was eaten, updates the score
            returns values score, reward and game over (boolean value true or false)
            """
            pass

        def is_collision(self):
            """
            checkss if snake has collided with itself or with the boundaries
            """
            pass

        def place_food(self):
            """
            places food on the screen
            if food is on snake body moves it elsewhere
            """
        def render():
            """
            renders the game window using pygame
            """
