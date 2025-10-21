import pygame
import numpy as np
from envs.snek import SnekEnv
from agents.agent import Agent

env = SnekEnv()

state_size = 11
action_size = 3

agent = Agent(state_size, action_size)

num_episodes = 1000
max_steps = 1000

pygame.init()
    screen = pygame.display.set_mode((env.width, env.height))
    clock = pygame.time.Clock()

for episode in range(num_episodes):
    state = env.reset()
    total_reward = 0
    done = False


    for step in range(max_steps):

        env.render(screen)
        clock.tick(10)

        action = agent.get_action(state)
        next_state, score, reward,done = env.play_step(action)
        agent.store(state, action, reward, next_state, done)
        agent.train()
        state = next_state
        total_reward += reward

        if done:
            break

        print(f"Episode {episode + 1}, Score: {score}, Total Reward: {total_reward}, Epsilon: {agent.epsilon:.3f}")



