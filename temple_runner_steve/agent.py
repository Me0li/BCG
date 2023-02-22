import os
import torch
import random
import cv2 as cv
import numpy as np
from time import time
from collections import deque

from model import Linear_QNet, QTrainer
from window_capture import WindowCapture
from calculations import Calculations, get_dict

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001 # learning rate

class Agent:
    def __init__(self):    
        self.n_games = 0 # gets incrementet after every 'game_over' and influence the tradeoff between exploration and exploitation
        self.epsilon = 0 # Parameter to control the randomness of the taken action
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        
        # Model:
        # Input state: [player, coin, obstacle, explosion, turnLeft, turnRight, player_coin_collision, player_obstacle_collision]
        self.model = Linear_QNet(8, 256, 2) # Input: 8-Variables State, 256 Layer, 2-Variables Output
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
    
    # --- Save data every loop for batch-training ---
    def remember(self, state, action, reward, next_state, game_over):       
        self.memory.append((state, action, reward, next_state, game_over))
    
    # --- Training based on a data-batch of played loops ---
    def train_long_memory(self):      
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # Get a random sample from memory, if BATCH_SIZE is exceeded => list of tuples
        else:
            mini_sample = self.memory
            
        states, actions, rewards, next_states, game_overs = zip(*mini_sample) # extract variables from mini_sample
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)
    
    # --- Training based on data of one played loop
    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)
    
    # --- Returns action ---
    # Starts with random moves (exploration). With every game_over, the chance to act based on learned knowledge increases (exploitation)
    def get_action(self, state):    
        self.epsilon = 80 - self.n_games # random moves: tradeoff exploration / exploitation
        action = [0, 0] # Left = [1,0], Right = [0,1]
        
        # move based on randomness => exploration
        if random.randint(0, 200) < self.epsilon:
            direction = random.randint(0, 1)
            action[direction] = 1
        # move based on trained model => exploitation
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            predicion = self.model(state0)
            direction = torch.argmax(predicion).item() # Convert the raw output of the DQN to max => example: raw = [5.0, 1.2] -> max = [1, 0]
            action[direction] = 1
            
        return action
    
def train():    
    # Create Yolov5-Model for object prediction
    yolo_model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp31/weights/best.pt', force_reload=True)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
      
    wincap = WindowCapture()
    calc = Calculations()
    agent = Agent()
    
    count_dooku = 0 # create a counter with a funny name
    phases = 0 # Decide between 'chose action'-phase and 'deal with consequences'-phase
    
    # Saves and repleces old model, if agent manages to life longer
    record = 0
    score = 0 # How many loops before game_over
        
    loop_time = time()
    
    while True:
        # 1) Take screenshot and predict object presence
        screenshot = wincap.get_screenshot()     # Take a screenshot of the desktop
        prediction = yolo_model(screenshot)      # Predict objects based on screenshot
        dataframe = prediction.pandas().xyxy[0]  # Transfigure prediction into dataframe
        one_frame_dict = get_dict(dataframe)     # Transfigure dataframe in a more manageable dictionary with needed variables: {<object_name>_idx: xmin, xmax}

        # Skip first 9 taken screenshots to give the agent time to act
        if count_dooku < 10:
            count_dooku += 1
        if count_dooku == 10 and phases == 0: # 'chose action'-phase
            
            # 2) Get old state (from calculations based on 10 frames) => example: [0,0,1,1,0 ...]
            state_old = calc.calculate_state(one_frame_dict)
        
            # 3) Get action => example: [1,0] = move left, [0,1] = move right
            action = agent.get_action(state_old)
        
            # 4) Execute actions in enviroment (through agent input)
            calc.execute_action(action)

            count_dooku = 0
            phases = 1
            
        if count_dooku == 10 and phases == 1: # 'deal with consequences'-phase
        
            # 5) Get new state (from calculations based on new 10 frames) => example: [0,0,1,1,0 ...]
            state_new = calc.calculate_state(one_frame_dict)
        
            # 6) Get reward and game_over (from calculations based on state_new)
            reward = calc.calculate_reward()
            game_over = calc.explosion
            
            # 7) Train shot term memory for one loop (with old state, action, new state, rewards and game_over)
            agent.train_short_memory(state_old, action, reward, state_new, game_over)
            
            # 8) Remeber the loop for long term memory training (with old state, action, new state, reward and game_over)
            agent.remember(state_old, action, reward, state_new, game_over)
    
            # 9) (Optional): Game Over
            if game_over:
                agent.n_games += 1
                agent.train_long_memory() # Train long term memory for a batch of remembered loops => experienced replay
                
                if record < score:
                    record = score
                    score = 0
                    agent.model.save()
                
            else:
                score += 1
            
            count_dooku = 0
            phases = 0

        # Show the object prediction in real time
        cv.imshow('Image Detection', np.squeeze(prediction.render()))

        # debug the loop rate
        print(f'FPS: {format(1 / (time() - loop_time))}')
        print(f'Objects in frame: {prediction.xyxy}\n')
        loop_time = time()

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break
        
if __name__ == '__main__':
    train()