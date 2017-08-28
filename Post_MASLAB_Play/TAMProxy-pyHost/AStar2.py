# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 12:45:19 2016

@author: arinz
"""
import SegmentDistances as SD
import PathPlanning as PP
import math
import matplotlib.pyplot as plt
import copy
import time

file1 = "Maps/Map1.txt"
file2 = "Maps/Map2.txt"
file3 = "Maps/green_map.txt"
file4 = "Maps/red_map.txt"
file5 = "Maps/Map3.txt"

tol = 1
delta = [[-1, 0 ], # go up
        [ 0, -1], # go left
        [ 1, 0 ], # go down
        [ 0, 1 ]] # go right
delta_name = ['^', '<', 'v', '>']
cost = 1 # the cost associated with moving from a cell to an adjacent one.

def search(init,goal,grid):
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1
    expand = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    action = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    x = init[0]
    y = init[1]
    g = 0
    h = calculatHeuristic((x,y),goal)
    f = g + h
    open = [[f, g, h, x, y]]
    found = False # flag that is set when search is complet
    resign = False # flag set if we can't find expand
    count = 0
    while not found and not resign:
        if len(open) == 0:
            resign = True
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[3]
            y = next[4]
            g = next[1]
            expand[x][y] = count
            count += 1
            if x == goal[0] and y == goal[1]:
                found = True
            else:
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            g2 = g + cost
                            h2 = calculatHeuristic((x2,y2),goal)
                            f2 = g2 + h2
                            open.append([f2, g2, h2, x2, y2])
                            closed[x2][y2] = 1
                            action[x2][y2] = i
    

        
#    print "expand"
#    for i in range(len(expand)):
#        print expand[i]
#    print "action"
#    for i in range(len(action)):
#        print action[i]

    policy = [[' '] * len(grid[0]) for i in grid]
    x = goal[0]
    y = goal[1]
    policy[x][y] = '*'
    while x != init[0] or y != init[1]:
        x2 = x - delta[action[x][y]][0]
        y2 = y - delta[action[x][y]][1]
        policy[x2][y2] = delta_name[action[x][y]]
        x = x2
        y = y2
#    print "solution"
#    for row in policy:
#        print row

    listOfPoints = []
    x = init[0]
    y = init[1]
    listOfPoints.append((x,y))
    while x != goal[0] or y != goal[1]:
        change = delta[delta_name.index(policy[x][y])]
        x += change[0]
        y += change[1]
        listOfPoints.append((x,y))

    #print "path:",listOfPoints
    return policy, listOfPoints

def convertCoordToGrid(coord,limits):
    xmin,xmax,ymin,ymax = limits
    ysize = ymax-ymin
    y = ysize - 1 - (coord[1]-ymin)
    x = coord[0]-xmin
    return x,y
#    return coord[0],coord[1]
    
def convertGridToCoord(gridcoord,limits):
    xmin,xmax,ymin,ymax = limits
    ysize = ymax-ymin
    y = ysize - 1 - gridcoord[1] + ymin
    x = gridcoord[0] + xmin
    return x,y
#    return gridcoord[0],gridcoord[1]
    
def makeGrid(limits, allSegments,tolerance=tol):
    xmin,xmax,ymin,ymax = limits
    xsize = xmax-xmin
    ysize = ymax-ymin
    grid = [[0 for row in range(ysize)] for col in range(xsize)]
    for x in range(xmin,xmax):
        for y in range(ymin,ymax):
            P = (x,y)
            for segment in allSegments:
                dist = SD.point_segment_distance(P,segment)
                if dist <= tolerance:
                    P2 = convertCoordToGrid(P,limits)
                    grid[P2[0]][P2[1]] = 1
                    break
#    for i in grid:
#        print i
    return grid
    

def solve1(fileName):
    #travels to blocks in order that they are in the file
    allSegments,graphForm,limits = PP.makeGraph(fileName)
    grid = makeGrid(limits, allSegments)
    allPolicies = []
    allPaths = []
    goals,start = PP.getGoalsStart(fileName)
    gridStart = convertCoordToGrid(start,limits)
    for block in goals:
        gridBlock = convertCoordToGrid(block,limits)
        policy, listOfPoints = search(gridStart,gridBlock,grid)
        allPolicies.append(policy)
        newListOfPoints = []
        for point in listOfPoints:
            newListOfPoints.append(convertGridToCoord(point,limits))
        allPaths.append(cleanPath(newListOfPoints,allSegments))
        gridStart = gridBlock
     
    lines = plt.plot(*graphForm)
    # use keyword args
    plt.setp(lines, color='r', linewidth=2.0)
    plt.axis(limits)
    
    xGoals = []
    yGoals = []
    for g in goals:
        xGoals.append(g[0])
        yGoals.append(g[1])
    stacks = plt.plot(xGoals,yGoals,'s')
    robot = plt.plot([start[0]],[start[1]],'*')
#    plt.show()
    
    overallPath = []
    for path in allPaths:
        overallPath = overallPath + path
        print path
        xVals = []
        yVals = []
        for coord in path:
            xVals.append(coord[0])
            yVals.append(coord[1])
        linePath = plt.plot(xVals,yVals)
        plt.setp(linePath, color='b', linewidth=1.0)
    print getPathLength(overallPath)

    
def solve2(fileName):
    #travels to blocks in order of which is closest straight line distance
    allSegments,graphForm,limits = PP.makeGraph(fileName)
    grid = makeGrid(limits, allSegments)
    allPolicies = []
    allPaths = []
    goals,start = PP.getGoalsStart(fileName)
    gridStart = convertCoordToGrid(start,limits)
    copyGoals = copy.deepcopy(goals)
    copyStart = copy.deepcopy(start)
    while len(copyGoals)>0:
        minDist = -1
        chosenBlock = None
        for block in copyGoals:
            dist = calculatHeuristic(copyStart,block)
            if minDist ==-1 or dist<minDist:
                minDist = dist
                chosenBlock = block
        gridBlock = convertCoordToGrid(chosenBlock,limits)
        policy, listOfPoints = search(gridStart,gridBlock,grid)
        allPolicies.append(policy)
        newListOfPoints = []
        for point in listOfPoints:
            newListOfPoints.append(convertGridToCoord(point,limits))
        allPaths.append(cleanPath(newListOfPoints,allSegments))
        gridStart = gridBlock
        copyGoals.remove(chosenBlock)
        copyStart = chosenBlock
     
    lines = plt.plot(*graphForm)
    # use keyword args
    plt.setp(lines, color='r', linewidth=2.0)
    plt.axis(limits)
    
    xGoals = []
    yGoals = []
    for g in goals:
        xGoals.append(g[0])
        yGoals.append(g[1])
    stacks = plt.plot(xGoals,yGoals,'s')
    robot = plt.plot([start[0]],[start[1]],'*')
#    plt.show()
    
    overallPath = []
    for path in allPaths:
        overallPath = overallPath + path
        print path
        xVals = []
        yVals = []
        for coord in path:
            xVals.append(coord[0])
            yVals.append(coord[1])
        linePath = plt.plot(xVals,yVals)
        plt.setp(linePath, color='b', linewidth=1.0)
    print getPathLength(overallPath)
    
def solve3(fileName):
    startTime = time.time()
    #travels to blocks based on what has the shortest path
    #greedy algorithm
    allSegments,graphForm,limits = PP.makeGraph(fileName)
    grid = makeGrid(limits, allSegments)
    allPolicies = []
    allPaths = []
    goals,start = PP.getGoalsStart(fileName)
    gridStart = convertCoordToGrid(start,limits)
    copyGoals = copy.deepcopy(goals)
    while len(copyGoals)>0:
        minDist = -1
        chosenBlock = None
        chosenPath = None
        chosenPolicy = None
        for block in copyGoals:
            gridBlock = convertCoordToGrid(block,limits)
            policy, listOfPoints = search(gridStart,gridBlock,grid)
            newListOfPoints = []
            for point in listOfPoints:
                newListOfPoints.append(convertGridToCoord(point,limits))
            clean = cleanPath(newListOfPoints,allSegments)
            dist = getPathLength(clean)
            if minDist ==-1 or dist<minDist:
                minDist = dist
                chosenBlock = block
                chosenPath = clean
                chosenPolicy = policy
        
        
        allPolicies.append(chosenPolicy)
        allPaths.append(chosenPath)
        gridStart = convertCoordToGrid(chosenBlock,limits)
        copyGoals.remove(chosenBlock)
     
    lines = plt.plot(*graphForm)
    # use keyword args
    plt.setp(lines, color='r', linewidth=2.0)
    plt.axis(limits)
    
    xGoals = []
    yGoals = []
    for g in goals:
        xGoals.append(g[0])
        yGoals.append(g[1])
    stacks = plt.plot(xGoals,yGoals,'s')
    robot = plt.plot([start[0]],[start[1]],'*')
#    plt.show()
    overallPath = []
    for path in allPaths:
        overallPath = overallPath + path
        print path
        xVals = []
        yVals = []
        for coord in path:
            xVals.append(coord[0])
            yVals.append(coord[1])
        linePath = plt.plot(xVals,yVals)
        plt.setp(linePath, color='b', linewidth=1.0)
    print getPathLength(overallPath)
    print "found in",(time.time()-startTime),"seconds"
    return overallPath
    
def calculatHeuristic(point,goal):
#    print point,goal
    return math.hypot(point[0]-goal[0], point[1]-goal[1])
    
def cleanPath(path,allSegments):
    start = 0
    end = 2
    path.reverse()
    while end<len(path)-1: 
        p1 = path[start]
        p2 = path[end]
        seg = (p1[0],p1[1],p2[0],p2[1])
        if isClearPath(seg,allSegments):
            path.pop(end-1)
        else:
            start += 1
            end += 1
    path.reverse()
    return path
        
def isClearPath(SEG, allSegments, tolerance = tol):
    for segment in allSegments:
        if SD.segments_distance(SEG, segment)<= tolerance:
            return False
    return True
    
def getPathLength(path):
    #a path is a list of points
    distance = 0.0
    for i in range(len(path)-1):
        distance += calculatHeuristic(path[i],path[i+1])
    return distance