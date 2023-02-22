import numpy as np
import win32gui
from PIL import ImageGrab
import cv2 as cv
import uuid     # Unique identifier
import os
import time as t
from sshkeyboard import listen_keyboard

class WindowCapture:

    # properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    c = 0

    # constructor
    def __init__(self, window_name=None):
        # find the handle for the window we want to capture.
        # if no window name is given, capture the entire screen
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))

        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):

        img = ImageGrab.grab(bbox=(0, 0, self.w, self.h))
        img_bgr = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)

        return img_bgr
    
    def collect_screenshots(self):
        IMAGES_PATH = os.path.join('data', 'images')    # /data/images
        labels = ['obstacle', 'coin', 'player', 'turnRight', 'turnLeft', 'explosion']
        number_imgs = 20

        # Loop through labels
        for label in labels:
            print('Collecting images for {}'.format(label))
            cv.waitKey(5)

            # Loop through image range
            for img_num in range (number_imgs):
                print('Collection images for {}, image number {}'.format(label, img_num))

                # Screen Feed
                img = ImageGrab.grab(bbox=(0, 0, self.w, self.h))

                # Naming out image path
                imgname = os.path.join(IMAGES_PATH, label+'.'+str(uuid.uuid1())+'.jpg')
                img.save(imgname)
                t.sleep(2)
        print('Done.')

    def collect_screenshots_keyPress(self):
        IMAGES_PATH = os.path.join('data', 'images')    # /data/images
        labels = ['turnRight', 'turnLeft', 'explosion']
        number_imgs = 20
        ct = 0

        def press(key):
            if key == "s":
                if self.c < 21:
                    print(f'Collection images for {labels[0]}, image number {self.c}')
                    # Screen Feed
                    img = ImageGrab.grab(bbox=(0, 0, self.w, self.h))

                    # Naming out image path
                    imgname = os.path.join(IMAGES_PATH, labels[0]+'.'+str(uuid.uuid1())+'.jpg')
                    img.save(imgname)
                    self.c += 1
                if self.c < 41 and self.c >= 20:
                    print(f'Collection images for {labels[1]}, image number {self.c}')
                    # Screen Feed
                    img = ImageGrab.grab(bbox=(0, 0, self.w, self.h))
        
                    # Naming out image path
                    imgname = os.path.join(IMAGES_PATH, labels[1]+'.'+str(uuid.uuid1())+'.jpg')
                    img.save(imgname)
                    self.c += 1
                if self.c < 61 and self.c >= 40:
                    print(f'Collection images for {labels[2]}, image number {self.c}')
                    # Screen Feed
                    img = ImageGrab.grab(bbox=(0, 0, self.w, self.h))
        
                    # Naming out image path
                    imgname = os.path.join(IMAGES_PATH, labels[2]+'.'+str(uuid.uuid1())+'.jpg')
                    img.save(imgname)
                    self.c += 1

        listen_keyboard(
            on_press=press
        )

        print('Done.') 

    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)