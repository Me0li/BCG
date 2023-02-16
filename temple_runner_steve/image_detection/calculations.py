import numpy as np
from pynput.keyboard import Key, Controller

class Calculations:
    def __init__(self):
        self.player = False
        self.player_cords = None
    
        self.coin = False
        self.coin_cords = None
    
        self.obstacle = False
        self.obstacle_cords = None
    
        self.explosion = False
    
        self.turnLeft = False
        self.turnLeft_cords = None
    
        self.turnRight = False
        self.turnRight_cords = None
    
        self.player_obstacle_collision = False
        self.player_coin_collision = False
        
        self.reward = 0

    def calculate_state(self, ten_frames):
        state = []
        # One dictionary with average values of ten captured frames
        ten_frames_average = self.average_ten_frames(ten_frames)
    
        # TODO: Check which entities are in frame
        for key, value in ten_frames_average.items():
            if 'player' in key:
                self.player = True
                self.player_cords = value
            if 'coin' in key:
                self.coin = True
                self.coin_cords = value
            if 'obstacle' in key:
                self.obstacle = True
                self.obstacle_cords = value
            if 'explosion' in key:
                self.explosion = True
            if 'turnLeft' in key:
                self.turnLeft = True
                self.turnLeft_cords = value
            if 'turnRight' in key:
                self.turnRight = True
                self.turnRight_cords = value
            
        # TODO: Caculate collision cours of player <-> coin
        if self.player == True and self.coin == True:
            player_coin_collision = self.collision_with_entity(self.player_cords, self.coin_cords)
            if self.player_coin_collision == True:
                self.reward = 5
            
        
        # TODO: Caculate collision cours of player <-> obstacle
        if self.player == True and self.obstacle == True:
            player_obstacle_collision = self.collision_with_entity(self.player_cords, self.obstacle_cords)
            if self.player_obstacle_collision == True:
                self.reward = -6
    
        # TODO: turnLeft
        # if (turnLeft_cords[1] - turnLeft_cords[0]) > # TODO: How big for turn?
    
        # TODO: turnRight
        # if (turnRight_cords[1] - turnRight_cords[0]) > # TODO: How big for turn?
    
        state.append(self.player)
        state.append(self.coin)
        state.append(self.obstacle)
        state.append(self.explosion)
        state.append(self.turnLeft)
        state.append(self.turnRight)
        state.append(self.player_coin_collision)
        state.append(self.player_obstacle_collision)

        return np.array(state, dtype=int)

    # Calculate the average of xmin and xmax of an object in ten frames
    def average_ten_frames(self, ten_frames_list):  
        cords = {}
        frames_len = len(ten_frames_list)
        for elem in ten_frames_list:
            if cords == {}:
                cords = elem
            else:
                cords = {key: [(cords[key][0] + elem[key][0]), (cords[key][1] + elem[key][1])] for key in cords}         
        cords = {key: [(cords[key][0] / frames_len), (cords[key][1] / frames_len)] for key in cords}
    
        return cords   
    
    # Check for collision
    def collision_with_entity(player, entity):
        if player[0] < entity[1] and player[1] > entity[1] \
            or player[0] < entity[0] and player[1] > entity[0]:
                return True
        return False
        

    # checks if List contains substring 'explosion' => returns bool
    def game_over(self, ten_frames_list):
        for elem in ten_frames_list:
            self.reward = -10
            return any([val for key, val in elem.items() if 'explosion' in key])
    
    # Press a key, based on given action
    def execute_action(self, action):
        keyboard = Controller()
    
        if action[0] == 1:
            keyboard.press(Key.left)
        if action[1] == 1:
            keyboard.press(Key.right)
        
    
'''
Call functions for debugging (remove later)
'''   

f1 = {
 'explosion_0': [1243.49365234375, 1275.8592529296875],
 'explosion_1': [1165.4423828125, 1195.5301513671875],
 'explosion_2': [1046.059326171875, 1069.9852294921875]
 }
f2 = {
 'explosion_0': [1243.49365234375, 1275.8592529296875],
 'explosion_1': [1165.4423828125, 1195.5301513671875],
 'explosion_2': [1046.059326171875, 1069.9852294921875]
  }
f3 = {
 'explosion_0': [1243.49365234375, 1275.8592529296875],
 'explosion_1': [1165.4423828125, 1195.5301513671875],
 'explosion_2': [1046.059326171875, 1069.9852294921875]
  }
f4 = {
 'explosion_0': [1243.49365234375, 1275.8592529296875],
 'explosion_1': [1165.4423828125, 1195.5301513671875],
 'explosion_2': [1046.059326171875, 1069.9852294921875]
  }

ten_frames_list = [f1, f2, f3, f4]

# game over = -10
# coin = +10
# collision with obstacle = -6
# collision with coin = +5
reward = 0


# average_ten_frames(ten_frames_list)
# print(game_over(ten_frames_list))