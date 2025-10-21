import random
import numpy as np
from collections import deque

class replay_buffer:
    def __init__(self, capacity = 10000):
        self.buffer = deque(maxlen = capacity)
    def push(self, state, reward,action, next_state,done):
        experience = (state, action, reward, next_state, done)
        self.buffer.append(experience)
    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, action, next_states, rewards, dones = zip(*batch)

        return (
            np.array(states),
            np.array(action),
            np.array(next_states),
            np.array(rewards),
            np.array(dones)
        )
    def __len__(self):
        return len(self.buffer)