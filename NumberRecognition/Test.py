# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 02:27:18 2017

@author: arinz
"""

try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract as tes
import cv2


#print (tes.pytesseract.tesseract_cmd)
tes.pytesseract.tesseract_cmd = "C:\\Users\\arinz\\Desktop\\WinPython-64bit-3.5.3.0Qt5\\Extras\\Tesseract-OCR\\tesseract"
#print (tes.pytesseract.tesseract_cmd)
results = tes.image_to_string(Image.open('numbers.png'),boxes=True)
print (results.split("\n"))
