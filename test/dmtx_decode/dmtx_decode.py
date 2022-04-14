#!/usr/bin/env python
import numpy as np
import cv2
from pylibdmtx import pylibdmtx

# has data matrix
image = cv2.imread('IMG_20211021_2212254.jpg', cv2.IMREAD_UNCHANGED)

# has not data matrix
#image = cv2.imread('bad.png', cv2.IMREAD_UNCHANGED)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

msg = pylibdmtx.decode(thresh)

#msg = pylibdmtx.decode(image)

print(msg)
#print(int(msg[0].data))
for i in msg:
    puid = i.data.decode("utf-8") 
    print(puid)
