import cv2 as cv
import numpy as np
from time import time
from myWindowcapture import WindowCapture

import os

import torch
import numpy as np

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
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp19/weights/last.pt', force_reload=True) 
#img = os.path.join('data', 'images', 'coin.4e67dcfe-a881-11ed-9fa9-2cf05d27a47e.jpg') 

while(True):
    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    results = model(screenshot)

    #cv.imshow('Image Detection', screenshot)
    imgResize = cv.resize(np.squeeze(results.render()), (1280, 720))
    cv.imshow('Image Detection', imgResize)

    # debug the loop rate
    print(f'FPS: {format(1 / (time() - loop_time))}')
    print(f'resultsxyxy: {results.xyxy}')
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')