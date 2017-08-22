# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 19:46:10 2017

@author: arinz
"""

import numpy as np
import cv2
import time
import copy

cap = cv2.VideoCapture(1)


imagePrefix = "C:/Users/arinz/Desktop/2016-2017/Spring/OpenCV Fun/Classifiers/Blocks/img/img"
imageSuffix = ".jpg"
numImages = 0
shouldCapture = False

stringToWrite = ""
while True:
    
    try:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Original", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print "couldn't take image"
        if shouldCapture:
            numImages += 1
            print numImages
            imageFileName = (imagePrefix + str(numImages) + imageSuffix)
            stringToWrite += (imageFileName + "\n")
            cv2.imwrite(imageFileName, frame);
            print imageFileName
            print "image captured"
            
    except KeyboardInterrupt:
        answer = raw_input("1.Toggle Capture\n2.Cancel\nYour choice: ")
        try:
            answer = int(answer)
            
        except ValueError:
            answer = 0
        if answer==1:
            shouldCapture = not shouldCapture
        elif answer==2:
            break
        else:
            continue
        
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

fp = open("bg.txt",'w')
fp.write(stringToWrite)
fp.close()