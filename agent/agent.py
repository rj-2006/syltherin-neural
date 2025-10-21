import torch
import torch.nn as nn
import random
import numpy as np
from .dqn import DQN
from replay_buffer import Replay_buffer

class Agent:
    def __init__(self, state_size, action_size, hidden_size=128, lr=0.001,
                 gamma=0.9, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01,
                 buffer_size=100_000, batch_size=64):

        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.batch_size = batch_size

        self.memory = Replay_buffer(buffer_size)
        self.model = DQN(state_size, hidden_size, action_size)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        self.loss = nn.MSELoss()

    def get_action(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.action_size)  # action index
        state = torch.tensor(state, dtype=torch.float).unsqueeze(0)
        q_values = self.model(state)
        return torch.argmax(q_values).item()

    def store(self, state, action, reward, next_state, done):
        self.memory.push(state, action, reward, next_state, done)

    def train(self):
        if len(self.memory) < self.batch_size:
            return

        states, actions, rewards, next_states, dones = self.memory.sample(self.batch_size)
        states = torch.tensor(states, dtype=torch.float)
        actions = torch.tensor(actions, dtype=torch.long)
        rewards = torch.tensor(rewards, dtype=torch.float)
        next_states = torch.tensor(next_states, dtype=torch.float)
        dones = torch.tensor(dones, dtype=torch.float)

        q_pred = self.model(states)
        q_pred = q_pred.gather(1, actions.unsqueeze(1)).squeeze(1)

        q_next = self.model(next_states).detach()
        q_target = rewards + self.gamma * torch.max(q_next, dim=1)[0] * (1 - dones)

        loss = self.loss(q_pred, q_target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
