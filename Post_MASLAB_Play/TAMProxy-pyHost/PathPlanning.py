# -*- coding: utf-8 -*-
"""
Created on Tue Feb 09 23:59:36 2016

@author: arinz
"""

import matplotlib.pyplot as plt
import SegmentDistances as SD

file1 = "Maps/Map1.txt"
file2 = "Maps/Map2.txt"
constant = 24 #24 inches per point

def getWalls(fileName):
    f = open(fileName)
    
    allSegments = []
    graphForm = []
    maxX = 0
    maxY = 0
    minX = 0
    minY = 0
    for line in f:
        if line[0] == "W" or line[0]=="P":
            parsed = line.split(',')
            segment = [constant*int(parsed[1]),constant*int(parsed[2]),constant*int(parsed[3]),constant*int(parsed[4])]
            xvals = [constant*int(parsed[1]),constant*int(parsed[3])]
            yvals = [constant*int(parsed[2]),constant*int(parsed[4])]
            allSegments.append(segment)
            graphForm.append(xvals)
            graphForm.append(yvals)
            if min(xvals)<=minX:
                minX = min(xvals)-constant
            if max(xvals)>=maxX:
                maxX = max(xvals)+constant
            if min(yvals)<=minY:
                minY = min(yvals)-constant
            if max(yvals)>=maxY:
                maxY = max(yvals)+constant
    bounds = (minX,maxX,minY,maxY)
    f.close()
    return allSegments, graphForm, bounds
    
def makeGraph(fileName):
    allSegments, graphForm, bounds = getWalls(fileName)
    lines = plt.plot(*graphForm)
    # use keyword args
    plt.setp(lines, color='r', linewidth=2.0)
    plt.axis(bounds)
#    plt.show()
    return allSegments,graphForm,bounds
    
def getGoalsStart(fileName):
    f = open(fileName)
    goals = []
    start = (0,0)
    for line in f:
        if line[0] == "L":
            parsed = line.split(',')
            start = (constant*int(parsed[1]),constant*int(parsed[2]))
        elif line[0] == "S":
            parsed = line.split(',')
            goals.append((constant*int(parsed[1]),constant*int(parsed[2])))
    return goals,start
#makeGraph(file1)
#makeGraph(file2)
#path = [(200, 200), (200, 199), (200, 195), (200, 170), (240, 120)]
#allSegments, graphForm, bounds = getWalls(file2)
#path.reverse()
#print path
#for i in range(len(path)):
#    for j in range(i,len(path)):
#        print path[i],path[j]
#        tempSeg = (path[i][0],path[i][1],path[j][0],path[j][1])
#        distances = []
#        for segment in allSegments:
#            distances.append(SD.segments_distance(tempSeg, segment))
#        print distances