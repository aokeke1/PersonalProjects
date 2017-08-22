# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 20:03:22 2016

@author: arinz
"""
import math

diameter = 3
circumference = math.pi*diameter
axel_length = 9.25
counts_per_rotation = 3200.0
def getAngles(leftEnc,rightEnc):
    left_arc = circumference*(leftEnc/counts_per_rotation) #number of rotations*circumference
    right_arc = circumference*(rightEnc/counts_per_rotation) #number of rotations*circumference
    angleEnc = math.degrees(((left_arc - right_arc)/axel_length)) #converted to degrees
    angleEnc2 = math.degrees(circumference*(leftEnc-rightEnc)/(counts_per_rotation*axel_length))
    print angleEnc,angleEnc2