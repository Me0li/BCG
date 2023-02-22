import numpy as np

from pynput.keyboard import Controller

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

    def calculate_state(self, frame):
        state = []
    
        # Check which entities are in frame
        for key, value in frame.items():
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
            
        # Caculate collision cours of player <-> coin
        if self.player and self.coin:
            player_coin_collision = self.collision_with_entity(self.player_cords, self.coin_cords)
        
        # Caculate collision cours of player <-> obstacle
        if self.player and self.obstacle:
            player_obstacle_collision = self.collision_with_entity(self.player_cords, self.obstacle_cords)
    
        state.append(self.player)
        state.append(self.coin)
        state.append(self.obstacle)
        state.append(self.explosion)
        state.append(self.turnLeft)
        state.append(self.turnRight)
        state.append(self.player_coin_collision)
        state.append(self.player_obstacle_collision)

        return np.array(state, dtype=int)
    
    # Measure Reward
    def calculate_reward(self):
        reward = 0
        if self.player_coin_collision:
            reward += 5
        if self.player_obstacle_collision:
            reward -= 6
        if self.explosion:
            reward -= 10
        return reward
    
    # Check for collision based on given bounding box parameters: xmin, xmax
    def collision_with_entity(player, entity):
        if player[0] < entity[1] and player[1] > entity[1] \
            or player[0] < entity[0] and player[1] > entity[0]:
                return True
        return False
    
    # Press a key, based on given action
    def execute_action(self, action):
        keyboard = Controller()
    
        if action[0] == 1:
            keyboard.press('a')
        if action[1] == 1:
            keyboard.press('d')
            
# return dic of cord of one frame
def get_dict(data_frame):
    
    obj_dict = {}
    
    for x in range(0, len(data_frame)):
        obj_dict[data_frame.at[x, 'name'] + f'_{x}'] = [data_frame.at[x, 'xmin'], data_frame.at[x, 'xmax']]
        
    return obj_dict