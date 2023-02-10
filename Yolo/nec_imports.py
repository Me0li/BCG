import torch
import os
from matplotlib import pyplot as plt
import numpy as np
import cv2
import time

# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp13/weights/last.pt', force_reload=True)

# img = "https://daily.jstor.org/wp-content/uploads/2017/12/traffic_jam_1050x700.jpg"
img = os.path.join('data', 'images', 'coin.4be4bd0a-a881-11ed-8e34-2cf05d27a47e.jpg')

results = model(img)
results.print()


cv2.imshow("tolles fenster", np.squeeze(results.render()))
cv2.waitKey(100000000)
