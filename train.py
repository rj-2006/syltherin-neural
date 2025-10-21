from envs.snek import SnekEnv
from agent.agent import Agent

env = SnekEnv()
state_size = 11
action_size = 3
agent = Agent(state_size, action_size)

num_episodes = 1000
max_steps = 1000

for episode in range(num_episodes):
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        action = agent.get_action(state)
        next_state, reward, done, score = env.play_step(action)
        agent.store(state, action, reward, next_state, done)
        agent.train()
        state = next_state
        total_reward += reward

    print(f"Episode {episode+1}, Score: {score}, Total Reward: {total_reward}, Epsilon: {agent.epsilon:.3f}")
