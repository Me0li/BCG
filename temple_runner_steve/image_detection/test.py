from mss import mss
import cv2
from PIL import Image
import numpy as np
from time import time

import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
print(screensize)

loop_time = time()

window = {'top': 100, 'left':200, 'width':1920, 'height':1080}

sct = mss()

while(True):
    
    sct_img = sct.grab(window)
    
    img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
    img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    cv2.imshow('Image Detection', np.array(img_bgr))
    
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()
    
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break