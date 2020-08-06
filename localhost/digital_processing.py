#
# Copyright (c) 2020 | Sathiyajith KS & Mathana Kumar S
#

# -*- coding: utf-8 -*-
"""digital_processing"""

import cv2
from PIL import Image

def threshAndConvert(imgpath):
  """
  The function to apply threshold to image
  Parameters: 
            imgpath(String): The path of image to which apply threshold. 
  """
  img = cv2.imread(imgpath)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
  cv2.imshow(gray)
  cv2.imwrite(imgpath, img)

#threshAndConvert("output/dataset1/1.jpg")