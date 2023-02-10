import cv2 as cv
import numpy as np
from time import time
from myWindowcapture import WindowCapture

import os

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

while(True):
    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    cv.imshow('Image Detection', screenshot)

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')