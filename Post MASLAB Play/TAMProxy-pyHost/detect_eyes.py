# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 20:41:25 2017

@author: arinz
"""

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

cap = cv2.VideoCapture(0)




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
    
face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_profileface.xml')
eye_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_eye.xml')
while True:
    
    try:
        ret, frame = cap.read()
        
#        print frame.shape
#        print ret
        if ret:
            
            frame2 = copy.copy(frame)
            gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            eyes = eye_cascade.detectMultiScale(gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(frame2,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            for (x,y,w,h) in faces:
                frame2 = cv2.rectangle(frame2,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame2[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

#            b,g,r = cv2.split(frame2) 
#            frame2[((r>(rg*g)) & (r>(rb*b)))] = [0,0,255]
#            frame2[((g>(gr*r)) & (g>(gb*b)))] = [0,255,0]
#            frame2[~(((g>(gr*r)) & (g>(gb*b)))|((r>(rg*g)) & (r>(rb*b))))] = [0,0,0]
#
#            
#            height, width, channels = frame2.shape
#            contours = filter_contours(frame2,height,width,ratio = 0.01)
#            boundingRectangles = []
#            for cnt in contours:
#                x,y,w,h = cv2.boundingRect(cnt)
#                cv2.rectangle(frame2,(x,y),(x+w,y+h),(255,255,255),2)
#                boundingRectangles.append((x,y,w,h))
            cv2.imshow("Original", frame)
            cv2.imshow("Filtered", frame2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print "couldn't take image"

            
    except KeyboardInterrupt:
        break
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
