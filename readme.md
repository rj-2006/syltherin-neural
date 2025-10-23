# Snake DQN Agent

## Overview
So, this project trains a Deep Q-Network (DQN) agent to play Snake using reinforcement learning. The agent learns to eat food and avoid collisions by trying actions and learning from rewards.

## How It Works

### Snake Environment
- Game state [an array]: 11 numbers (dangers, direction, food location).
- Actions [another array]: Straight, turn right, turn left. [0,1,2]
- Rewards: Eat food = +10, crash = -10.

### Neural Network
- Takes 11 inputs, processes through 128 neurons (with ReLU to avoid learning issues), outputs 3 Q-values.
- Picks highest Q-value for action.
- Learns by comparing predictions to real rewards. [loss function is msv]

### Replay Buffer
- Saves game experiences (state, action, reward, next state).
- Randomly samples 64 at a time to train, keeping learning stable.

#### Why does it sample randomly you say?

Contigous samples would be like expecting the episode to repeat which is like not learning from your mistakes. (a bummer)

### Agent
- Starts exploring (random actions), shifts to exploiting (best actions).
  #### How you may ask?
   The epsilon and epsilon decay handle it. the exploration rate is controlled by epsilon value intially set to 1, epsilon decay per state 0.995 when it starts learnin using the dnq model.

- Updates brain using past experiences. (using the replay_buffer)

### Training
- Plays 1000 games, each up to 1000 moves.
- Learns after each move, prints score and progress.

## Math Behind It
Uses Q-learning update:

(the bellman equation if you really want to see the math)
```
Q(s, a) = reward + gamma * max Q(next_state, all_actions)
```
- Q(s,a): Action value in current state.
- reward: Points from move.
- gamma (0.9): Future rewards discounted.
- max Q(...): Best value from next state.

Network minimizes error between predicted and actual Q-values.

## Installation
```
pip install torch pygame numpy
```

## Usage
```
python train.py
```
Watch the game window; see progress in console. :)
