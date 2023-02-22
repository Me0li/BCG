import os
from window_capture import WindowCapture

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