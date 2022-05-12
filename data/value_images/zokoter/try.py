import numpy as np
import cv2
import os

tmplt = cv2.imread("./data/value_images/4.png", 0)
img = cv2.imread("tthisss.png", 0)

match = cv2.matchTemplate(img, tmplt, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
print(max_val, min_val)
