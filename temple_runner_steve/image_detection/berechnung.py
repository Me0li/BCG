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

# checks if List contains substring 'explosion' => returns bool
def check_go(ten_frames_list):
    for elem in ten_frames_list:
        reward = -10
        return any([val for key, val in elem.items() if 'explosion' in key])
        
# Calculate the average of xmin and xmax of an object in ten frames
def average_ten_frames(ten_frames_list):   
    cords = {}
    frames_len = len(ten_frames_list)
    for elem in ten_frames_list:
        if cords == {}:
            cords = elem
        else:
            cords = {key: [(cords[key][0] + elem[key][0]), (cords[key][1] + elem[key][1])] for key in cords}         
    cords = {key: [(cords[key][0] / frames_len), (cords[key][1] / frames_len)] for key in cords}
    
    # print(cords) # DEBUGGING: remove later
    
# Check for collision
def collision(ten_frames_list):
    pass

    
'''
Call functions for debugging (remove later)
'''
    
average_ten_frames(ten_frames_list)

print(check_go(ten_frames_list))