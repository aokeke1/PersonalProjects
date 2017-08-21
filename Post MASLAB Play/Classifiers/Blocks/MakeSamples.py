# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 19:46:10 2017

@author: arinz
"""

import numpy as np
import cv2
import time
import copy

rg = 1.7
rb = 1.7
gr = 1.1
gb = 1.1

cap = cv2.VideoCapture(1)


imagePrefix = "C:/Users/arinz/Desktop/2016-2017/Spring/OpenCV_Fun/Classifiers/Blocks/img2/img"
imagePrefix2 = "C:/Users/arinz/Desktop/2016-2017/Spring/OpenCV_Fun/Classifiers/Blocks/img3/img"
imageSuffix = ".jpg"
numImages = 0
shouldCapture = False

stringToWrite = ""

def filter_contours(frame,height,width,ratio = 0.01):
    """
    returns real contours, sorted with the biggest contour as the first element
    """
    imgray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,50,255,0)
    if ret==False:
        return []
    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    minArea = ratio*height*width
    realContours = []
    for cnt in contours:
        cntArea = cv2.contourArea(cnt)
        if cntArea>=minArea:
            realContours.append(cnt)
        else:
            frame = cv2.drawContours(frame,[cnt],0,[0,0,0],-1)
            
    sortedCnts = sorted(realContours,key=cv2.contourArea)
    sortedCnts.reverse()
    return sortedCnts

while True:
    
    try:
        ret, frame = cap.read()
        if ret:
            
            frame2 = copy.copy(frame)
            b,g,r = cv2.split(frame2) 
            frame2[((r>(rg*g)) & (r>(rb*b)))] = [0,0,255]
            frame2[((g>(gr*r)) & (g>(gb*b)))] = [0,255,0]
            frame2[~(((g>(gr*r)) & (g>(gb*b)))|((r>(rg*g)) & (r>(rb*b))))] = [0,0,0]

            
            height, width, channels = frame2.shape
            contours = filter_contours(frame2,height,width,ratio = 0.01)
            boundingRectangles = []
            for cnt in contours:
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(frame2,(x,y),(x+w,y+h),(255,255,255),2)
                boundingRectangles.append((x,y,w,h))
            cv2.imshow("Original", frame)
            cv2.imshow("Filtered", frame2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print "couldn't take image"
        if shouldCapture and len(boundingRectangles)>0:
            #get bounding rectangles
            numImages += 1
            print numImages
            imageFileName = (imagePrefix + str(numImages) + imageSuffix)
            imageFileName2 = (imagePrefix2 + str(numImages) + imageSuffix)
            imageInfo = imageFileName + "\t" + str(len(boundingRectangles))
            for i in range(len(boundingRectangles)):
                r = boundingRectangles[i]
                print r
                imageInfo += "\t" + str(r).replace("(","").replace(")","").replace(",","")
            print imageInfo
            stringToWrite += (imageInfo + "\n")
            cv2.imwrite(imageFileName, frame);
            cv2.imwrite(imageFileName2, frame2);
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

fp = open("info.dat",'w')
fp.write(stringToWrite)
fp.close()