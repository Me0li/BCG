import os
from time import time
import torch
import random
import numpy as np
import cv2 as cv

from collections import deque
from myImageDetection import get_ten_frames
from calculations import Calculations
from model import Linear_QNet, QTrainer

from myWindowcapture import WindowCapture
from read_output import get_BB_cords

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self) -> None:
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(8, 256, 2) # Input: 8 States, 256 Layer, 2 Outputs
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
    
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
            move = random.randint(0, 1)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            predicion = self.model(state0)
            move = torch.argmax(predicion).item()
            final_move[move] = 1
        
        return final_move
    
def train():
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    wincap = WindowCapture()
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp22/weights/last.pt', force_reload=True)
    loop_time = time()
        
    agent = Agent()
    calc = Calculations()

    # Execution:
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
    '''
    while True:
        # 1) Get 10 frames (from CNN)
        ten_frames = get_ten_frames()
        
        # 2) Get old state (from calculations based on 10 frames) => example: [0,0,1,1,0 ...]
        state_old = calc.calculate_state(ten_frames)
        
        # 3) Get action (from DQN with old state) => example: [1,0] = move left, [0,1] = move right
        action = agent.get_action(state_old)
        
        # 4) + 5) Execute actions in enviroment (through agent input)
        calc.execute_action(action)
        
        # 6) Get new 10 frames (from CNN)
        ten_frames.clear()
        ten_frames = get_ten_frames()
        
        # 7) Get new state (from calculations based on new 10 frames) => example: [0,0,1,1,0 ...]
        state_new = calc.calculate_state(ten_frames)
        
        # 8) Get reward and game_over (from calculations based on state_new)
        reward = calc.reward
        game_over = calc.explosion
            
        # 8) Train shot term memory (with old state, old action, new state, rewards and game_over)
        agent.train_short_memory(state_old, action, reward, state_new, game_over)
            
        # 9) Remeber memory (with old state, old action, new state, reward and game_over)
        agent.remember(state_old, action, reward, state_new, game_over)
    
        # 10) (Optional): Game Over
        if game_over:
            agent.n_games += 1
            agent.train_long_memory()
            
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break
    '''

    ten_frames = []
    phases = 0

    while(True):
        
        # get an updated image of the game
        screenshot = wincap.get_screenshot()
        results = model(screenshot)
        re_def = results.pandas().xyxy[0]
        one_frame = get_BB_cords(re_def)

        if len(ten_frames) < 10:
            ten_frames.append(one_frame)
        elif (len(ten_frames) >= 10 and phases == 0):
            
            # 2) Get old state (from calculations based on 10 frames) => example: [0,0,1,1,0 ...]
            state_old = calc.calculate_state(ten_frames)
        
            # 3) Get action (from DQN with old state) => example: [1,0] = move left, [0,1] = move right
            action = agent.get_action(state_old)
        
            # 4) + 5) Execute actions in enviroment (through agent input)
            calc.execute_action(action)

            ten_frames.clear()
            phases = 1
            
        if (len(ten_frames) >= 10 and phases == 1):
        
            # 7) Get new state (from calculations based on new 10 frames) => example: [0,0,1,1,0 ...]
            state_new = calc.calculate_state(ten_frames)
        
            # 8) Get reward and game_over (from calculations based on state_new)
            reward = calc.reward
            game_over = calc.explosion
            
            # 8) Train shot term memory (with old state, old action, new state, rewards and game_over)
            agent.train_short_memory(state_old, action, reward, state_new, game_over)
            
            # 9) Remeber memory (with old state, old action, new state, reward and game_over)
            agent.remember(state_old, action, reward, state_new, game_over)
    
            # 10) (Optional): Game Over
            if game_over:
                agent.n_games += 1
                agent.train_long_memory()
                
            ten_frames.clear()
            phases = 0

        #cv.imshow('Image Detection', np.squeeze(results.render()))
        imgResize = cv.resize(np.squeeze(results.render()), (1280, 720))
        cv.imshow('Image Detection', imgResize)

        # debug the loop rate
        print(f'FPS: {format(1 / (time() - loop_time))}')
        print(f"resultsxyxy: {results.xyxy}")
        loop_time = time()

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break
        
if __name__ == '__main__':
    train()