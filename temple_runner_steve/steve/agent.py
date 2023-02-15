import os
import torch
import random
import numpy as np

from collections import deque
# TODO: Imports from image_detection
from image_detection.myImageDetection import get_ten_frames
from image_detection.calculations import calculate_state

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self) -> None:
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        # self.model = Linear_QNet(11, 256, 3)
        # TODO: Trainer ?
        
    def get_state(self):
        state = [
            # TODO: Caclulate collision cours of player <-> obstacle
            
            # TODO: Caclulate collision cours of player <-> coin
        
            # TODO: Given entities in ten frames
        
            # TODO: Arrow Left/Right
            
        ]
        
        return np.array(state, dtype=int)
    
    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))
        
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
            
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)
    
        
    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)
    
    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            predicion = self.model(state0)
            move = torch.argmax(predicion).item()
            final_move[move] = 1
        
        return final_move
    
def train():
        
    agent = Agent()
    # TODO: Create model variable
        
        
    # TODO:
    # 1) Get 10 frames (from CNN)
    # 2) Get old state (from calculations based on 10 frames) => example: [0,0,1,1,0 ...]
    # 3) Get old action (from DQN with old state) => example: [1,0] = move left, [0,1] = move right
    # 4) Execute actions in enviroment (through agent input)
    # 5) Get rewards and game_over ()
    # 6) Get new 10 frames (from CNN)
    # 7) Get new state (from calculations based on new 10 frames) => example: [0,0,1,1,0 ...]
    # 8) Train shot term memory (with old state, old action, new state, rewards and game_over)
    # 9) Remeber memory (with old state, old action, new state, reward and game_over)
    # if game_over
        
    while True:
        # 1) Get 10 frames (from CNN)
        ten_frames = get_ten_frames()
        
        # 2) Get old state (from calculations based on 10 frames) => example: [0,0,1,1,0 ...]
        state_old = calculate_state(ten_frames)
        
        '''
        # 3) Get action (from DQN with old state) => example: [1,0] = move left, [0,1] = move right
        action = get_action()
            
        # 4) + 5) Execute actions in enviroment (through agent input)
        execute_action(action)
        '''    
        
        # 6) Get new 10 frames (from CNN)
        ten_frames.clear()
        ten_frames = get_ten_frames()
        
        
        # 7) Get new state (from calculations based on new 10 frames) => example: [0,0,1,1,0 ...]
        state_new = calculate_state(ten_frames)
        
        '''
        # 8) Get reward and game_over (from calculations based on state_new)
        reward = get_reward()
        game_over = get_game_over()
            
        # 8) Train shot term memory (with old state, old action, new state, rewards and game_over)
        agent.train_short_memory(state_old, action, state_new, reward, game_over)
            
        # 9) Remeber memory (with old state, old action, new state, reward and game_over)
        agent.remember(state_old, action, state_new, reward, game_over)
    
        # 10) (Optional): Game Over
        if game_over:
            agen.train_long_memory()
            
            
        '''
            
        pass
    pass