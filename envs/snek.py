import pygame
import random
import numpy as np
from enum import Enum
from collections import namedtuple

Point = namedtuple('Point', 'x,y')
BLOCK_SIZE = 20
SPEED = 10

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnekEnv:

    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        pygame.init()
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake RL')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.width // 2, self.height // 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame = 0
        return self.get_state()

    def _place_food(self):
        x = random.randint(0, (self.width // BLOCK_SIZE) - 1) * BLOCK_SIZE
        y = random.randint(0, (self.height // BLOCK_SIZE) - 1) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame += 1
        reward = 0
        done = False

        # 1) Move
        self._move(action)
        self.snake.insert(0, self.head)

        # 2) Check collision
        if self.is_collision():
            done = True
            reward = -10
            return self.get_state(), reward, done, self.score

        # 3) Check food
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # 4) Render
        self._update_ui()
        self.clock.tick(SPEED)

        return self.get_state(), reward, done, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt.x < 0 or pt.x >= self.width or pt.y < 0 or pt.y >= self.height:
            return True
        if pt in self.snake[1:]:
            return True
        return False

    def _move(self, action):
        # action = 0: straight, 1: right, 2: left
        clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clockwise.index(self.direction)

        if action == 0:  # straight
            new_dir = clockwise[idx]
        elif action == 1:  # right turn
            new_dir = clockwise[(idx + 1) % 4]
        else:  # left turn
            new_dir = clockwise[(idx - 1) % 4]

        self.direction = new_dir

        x, y = self.head
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)

    def get_state(self):
        head = self.head
        point_l = Point(head.x - BLOCK_SIZE, head.y)
        point_r = Point(head.x + BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y - BLOCK_SIZE)
        point_d = Point(head.x, head.y + BLOCK_SIZE)

        dir_l = self.direction == Direction.LEFT
        dir_r = self.direction == Direction.RIGHT
        dir_u = self.direction == Direction.UP
        dir_d = self.direction == Direction.DOWN

        danger_straight = (dir_r and self.is_collision(point_r)) or \
                          (dir_l and self.is_collision(point_l)) or \
                          (dir_u and self.is_collision(point_u)) or \
                          (dir_d and self.is_collision(point_d))

        danger_right = (dir_u and self.is_collision(point_r)) or \
                       (dir_d and self.is_collision(point_l)) or \
                       (dir_l and self.is_collision(point_u)) or \
                       (dir_r and self.is_collision(point_d))

        danger_left = (dir_d and self.is_collision(point_r)) or \
                      (dir_u and self.is_collision(point_l)) or \
                      (dir_r and self.is_collision(point_u)) or \
                      (dir_l and self.is_collision(point_d))

        food_left = self.food.x < self.head.x
        food_right = self.food.x > self.head.x
        food_up = self.food.y < self.head.y
        food_down = self.food.y > self.head.y

        state = np.array([
            danger_straight,
            danger_right,
            danger_left,
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            food_left,
            food_right,
            food_up,
            food_down
        ], dtype=int)

        return state

    def _update_ui(self):
        self.display.fill((0, 0, 0))

        for pt in self.snake:
            pygame.draw.rect(self.display, (0, 255, 0), pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(self.display, (255, 0, 0), pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.flip()
