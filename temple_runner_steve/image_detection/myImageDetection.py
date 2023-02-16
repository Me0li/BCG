import cv2 as cv
import numpy as np
from time import time
from myWindowcapture import WindowCapture

import os

import torch
from matplotlib import pyplot as plt
import numpy as np

from read_output import get_BB_cords

# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Change the working directory to the folder this script is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# initialize the WindowCapture class
wincap = WindowCapture()

# List all Windows if you want to capture a specific window
# myWindows = WindowCapture.list_window_names()
# print(myWindows)

# Collect 20 Screenshots of each label
# wincap.collect_screenshots()
# exit()

# Collect 20 Screenshots of each label
# wincap.collect_screenshots_keyPress()
# exit()

loop_time = time()
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp14/weights/last.pt', force_reload=True) 
#img = os.path.join('data', 'images', 'coin.4e67dcfe-a881-11ed-9fa9-2cf05d27a47e.jpg') 

global_list = []

def get_ten_frames():
   ten_frames = []
   
   screenshot = wincap.get_screenshot()
   results = model(screenshot)    
   re_def = results.pandas().xyxy[0]
   print(f'The type is: {type(re_def)}')
   one_frame = get_BB_cords(re_def)
   
   while len(ten_frames) < 10:
      ten_frames.append(one_frame)
      
   return ten_frames
'''
while(True):
    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    results = model(screenshot)
    
    re_def = results.pandas().xyxy
    one_frame = get_BB_cords(re_def)

    if len(global_list) < 10:
       global_list.append(one_frame)
    else:
       # average_ten_frames(global_list)
       # print("----------------------------------------------------------------------")
       global_list.clear()
       # print(f'global_list: {len(global_list)}')
       global_list.append(one_frame)

    #cv.imshow('Image Detection', screenshot)
    cv.imshow('Image Detection', np.squeeze(results.render()))

    # debug the loop rate
    print(f'FPS: {format(1 / (time() - loop_time))}')
    print(f"resultsxyxy: {results.xyxy}")
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')

'''