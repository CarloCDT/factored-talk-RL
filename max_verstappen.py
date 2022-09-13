from CarRacingAgents import CarRacingAgent
import gym
from collections import deque
import numpy as np

def run_max(track_num):
    
    agent = CarRacingAgent(name = 'agent_max')
    agent.load('trained_agents/agent_max.h5')
    agent.epsilon = 0 # Set epsilon to 0

    env = gym.make('CarRacing-v2', continuous=False, render_mode = 'human')

    init_state = env.reset(seed=track_num)[0]
    init_state = agent.process_state_image(init_state, env)

    total_reward = 0
    state_frame_stack_queue = deque([init_state]*agent.frame_stack_num, maxlen=agent.frame_stack_num)

    steps = 0
    done = False

    while not done:

        steps+=1
        
        current_state_frame_stack = agent.generate_state_frame_stack_from_queue(state_frame_stack_queue)
        action = agent.act(current_state_frame_stack)
        next_state, reward, done, truncated, info = env.step(action)

        total_reward += reward

        next_state = agent.process_state_image(next_state, env)
        state_frame_stack_queue.append(next_state)

        if done or steps==999:
            env.close()
            return total_reward
