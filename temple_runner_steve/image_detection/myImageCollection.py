import cv2 as cv
import numpy as np
from time import time
import time as t

from PIL import ImageGrab

import torch
from matplotlib import pyplot as plt

import uuid                             # Unique identifier
import os

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
        img = ImageGrab.grab(bbox=(0, 0, 1280, 720))

        # Naming out image path
        imgname = os.path.join(IMAGES_PATH, label+'.'+str(uuid.uuid1())+'.jpg')
        img.save(imgname)
        t.sleep(2)
print('Done.')