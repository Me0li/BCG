import os
import cv2
import torch
import numpy as np

# Load model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp31/weights/last.pt', force_reload=True)

# Load test image
img = os.path.join('data', 'images', 'coin.3ccbc13b-a881-11ed-bd69-2cf05d27a47e.jpg')

results = model(img)
results.print()

imgResize = cv2.resize(np.squeeze(results.render()), (1280, 720))
cv2.imshow('Image Detection', imgResize)
cv2.waitKey(100000000)