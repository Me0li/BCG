import torch
import os
from matplotlib import pyplot as plt
import numpy as np
import cv2
import time
from read_output import get_BB_cords
#from berechnung import check_go

# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp22/weights/last.pt', force_reload=True)

# img = "https://daily.jstor.org/wp-content/uploads/2017/12/traffic_jam_1050x700.jpg"
img = os.path.join('data', 'images', 'coin.3ccbc13b-a881-11ed-bd69-2cf05d27a47e.jpg')

results = model(img)
results.print()

re_df = results.pandas().xyxy[0]
one_frame = get_BB_cords(re_df)
print(one_frame)

# print(check_go(one_frame))


imgResize = cv2.resize(np.squeeze(results.render()), (1280, 720))
cv2.imshow('Image Detection', imgResize)
cv2.waitKey(100000000)