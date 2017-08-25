# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 02:05:30 2017

@author: arinz
"""
import numpy as np
import cv2
#Pins
left_encoder_pins = (8,9) #(white,yellow)
right_encoder_pins = (6,7) #(white,yellow)
left_motor_pins = (2,3) #(dir,pwm)
right_motor_pins = (4,5) #(dir,pwm)

#Dead reckoning
axel_length = 9.5 #distance between two wheels
wheel_radius = 1.25 #radius of wheels
wheel_circumference = 2*wheel_radius*np.pi
counts_per_rotation = 3200

#PID
maxTurnSpeed = 50
largeAngle = 10
kP = 2
kI = 1e-3
kD = 110

#Parameters for webcam
webcamNumber = 1
webcamWidth = 640
webcamHeight = 480
CAMERA_CENTER = (webcamWidth/2,webcamHeight/2)

maxDriveSpeed = 60

#Image Processing
rg = 1.7
rb = 1.7
gr = 1.1
gb = 1.1
obj_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_eye.xml')

desiredCodeArea = 5
desiredData = "shoes"
resetImageTime = 1000 #milliseconds
