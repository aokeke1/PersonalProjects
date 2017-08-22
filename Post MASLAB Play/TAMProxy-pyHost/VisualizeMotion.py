# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 15:09:47 2016

@author: arinz
"""

import math,time,copy
import SegmentDistances as SD
from graphics import *

file1 = "Maps/Map1.txt"
file2 = "Maps/Map2.txt"
file3 = "Maps/green_map.txt"
file4 = "Maps/red_map.txt"
file5 = "Maps/Map3.txt"
constant = 24. #24 inches per unit length in map
tol = max(range(6))
delta = .2*constant

def getWalls(fileName,constant=constant):
    f = open(fileName)
    
    allWalls = []
    allPlatforms = []
    
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
            if line[0]=="W":
                allWalls.append(segment)
            elif line[0]=="P":
                allPlatforms.append(segment)
            if min(xvals)<=minX:
                minX = min(xvals)-constant
            if max(xvals)>=maxX:
                maxX = max(xvals)+constant
            if min(yvals)<=minY:
                minY = min(yvals)-constant
            if max(yvals)>=maxY:
                maxY = max(yvals)+constant
    bounds = (int(minX),int(maxX),int(minY),int(maxY))
    f.close()
    allSegments = allWalls + allPlatforms
    return bounds, allWalls, allPlatforms, allSegments

def getGoalsStart(fileName,constant=constant):
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
    f.close()
    return goals,start

def initializeWindow(fileName,delta=delta):
    
    bounds, wallSegsNoPlat, platformSegs, allSegments = getWalls(fileName)
    win = GraphWin('RobotTracking', (bounds[1]-bounds[0]), (bounds[3]-bounds[2]))
    win.setCoords(bounds[0], bounds[2], bounds[1], bounds[3])
    allWalls = []
    allPlats = []
    for segment in wallSegsNoPlat:
        wall = Line(Point(segment[0], segment[1]), Point(segment[2], segment[3])) # set endpoints
        wall.setWidth(3)
        wall.setFill("blue")
        wall.draw(win)
        allWalls.append(wall)
    for segment in platformSegs:
        plat = Line(Point(segment[0], segment[1]), Point(segment[2], segment[3])) # set endpoints
        plat.setWidth(3)
        plat.setFill("purple")
        plat.draw(win)
        allPlats.append(plat)
        
    goals,start = getGoalsStart(fileName)
    
    allBlocks = []
    blockCenters = []
    for goal in goals:
        topCorner = Point(goal[0]+delta,goal[1]+delta)
        bottomCorner = Point(goal[0]-delta,goal[1]-delta)
        block = Rectangle(topCorner, bottomCorner)
        block.setFill('green')
        block.draw(win)
        allBlocks.append(block)
        blockCenters.append(Point(goal[0],goal[1]))

    corners = [Point(start[0],start[1]+delta),Point(start[0]-delta/2,start[1]-delta),Point(start[0]+delta/2,start[1]-delta)]
    robot = Polygon(*corners)
    robot.setFill('red')
    robot.draw(win)
    robotCenter = Point(start[0],start[1])
    robotCenter.setFill('white')
    robotCenter.draw(win)
#    currentTheta = math.pi/2
#    deltaTheta = 1.0/1
#    distance = 20.0/1
#    initTime = time.time()
#    
#    while True:
#        if time.time() - initTime>1:
##            pass
#            print "moved"
#            initTime = time.time()
#            currentTheta += deltaTheta
#            robot = rotateTriangle(robot,robotCenter,deltaTheta,win)
#            moveTriangle(robot,robotCenter,distance,currentTheta,win)
    
    return win,bounds,allWalls,allPlats,allSegments,wallSegsNoPlat,platformSegs,allBlocks,robot,robotCenter

def rotateRobot(triangle,center,deltaTheta,win):
    #rotates a triangle a certain deltaTheta radians
    points = triangle.getPoints()
    newPoints = []
    for point in points:
        x2 = center.getX() + (point.getX() - center.getX())*math.cos(deltaTheta) - (point.getY() - center.getY())*math.sin(deltaTheta)
        y2 = center.getY() + (point.getY() - center.getY())*math.cos(deltaTheta) + (point.getX() - center.getX())*math.sin(deltaTheta)
        newPoints.append(Point(x2,y2))
    triangle.undraw()
    center.undraw()
    robot = Polygon(*newPoints)
    robot.setFill('red')
    robot.draw(win)
    center.draw(win)
    return robot
    
def moveRobot(robot,center,distance,theta,win):
    #moves a triangle a difstance in a direction theta
    dx = distance * math.cos(theta)
    dy = distance * math.sin(theta)
    oldCenter = center.clone()
    
    robot.move(dx,dy)
    center.move(dx,dy)
    #make trail
    trail = Line(oldCenter,center) # set endpoints
    trail.setWidth(1)
    trail.setFill('blue')
    trail.draw(win)

def moveRobot2(robot,center,newSpot):
    #moves a triangle a difstance in a direction theta
    dx = newSpot.getX() - center.getX()
    dy = newSpot.getY() - center.getY()
    oldCenter = center.clone()
    
    robot.move(dx,dy)
    center.move(dx,dy)
    #make trail
    trail = Line(oldCenter,center) # set endpoints
    trail.setWidth(1)
    trail.setFill('orange')
    trail.draw(win)

#Path planning
def getPath(win,grid,limits,allBoundries,allSegments,allBlocks,robot,robotCenter,tolerance = tol):#,finalPathLines = None):
    if len(allBlocks)==0:
        return None
#    if finalPathLines != None:
#        for line in finalPathLines:
#            line.undraw()
    start = (robotCenter.getX(),robotCenter.getY())
    gridStart = convertCoordToGrid(start,limits)
    minDist = -1
    chosenBlock = None
    chosenPath = None
    chosenPolicy = None
    for block in allBlocks:
        blockcoord = (block.getCenter().getX(),block.getCenter().getY())
        gridBlock = convertCoordToGrid(blockcoord,limits)
        policy, listOfPoints = search(gridStart,gridBlock,grid)
        newListOfPoints = []
        for point in listOfPoints:
            newListOfPoints.append(convertGridToCoord(point,limits))
        clean = cleanPath(newListOfPoints,allSegments,tolerance = tolerance)
        dist = getPathLength(clean)
        if minDist ==-1 or dist<minDist:
            minDist = dist
            chosenBlock = block
            chosenPath = clean
            chosenPolicy = policy
    #Convert to using point objects
    finalPath = []
#    finalPathLines = []
    for p in chosenPath:
        finalPath.append(Point(p[0],p[1]))
    #draw in the desired path
    for i in range(len(finalPath)-1):
        pathSegment = Line(finalPath[i],finalPath[i+1])
        pathSegment.setWidth(1)
        pathSegment.setFill("green")
        pathSegment.draw(win)
#        finalPathLines.append(pathSegment)

    return chosenBlock,finalPath#,finalPathLines
    
def calculatHeuristic(point,goal):
    return math.hypot(point[0]-goal[0], point[1]-goal[1])
    
def cleanPath(path,allSegments,tolerance=tol):
    start = 0
    end = 2
    path.reverse()
    while end<len(path)-1: 
        p1 = path[start]
        p2 = path[end]
        seg = (p1[0],p1[1],p2[0],p2[1])
        if isClearPath(seg,allSegments,tolerance=tolerance):
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
#        P1 = (path[i].getX(),path[i].getY())
#        P2 = (path[i+1].getX(),path[i+1].getY())
#        distance += calculatHeuristic(P1,P2)
    return distance




def search(init,goal,grid,cost=1):
    init = (int(init[0]),int(init[1]))
    goal = (int(goal[0]),int(goal[1]))
    delta = [[-1, 0 ], # go up
            [ 0, -1], # go left
            [ 1, 0 ], # go down
            [ 0, 1 ]] # go right
    delta_name = ['^', '<', 'v', '>']
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
    
def convertGridToCoord(gridcoord,limits):
    xmin,xmax,ymin,ymax = limits
    ysize = ymax-ymin
    y = ysize - 1 - gridcoord[1] + ymin
    x = gridcoord[0] + xmin
    return x,y
    
def makeGrid(limits, allSegments,tolerance=tol):
    startTime = time.time()
    xmin,xmax,ymin,ymax = limits
    xsize = xmax-xmin
    ysize = ymax-ymin
    grid = [[0 for row in range(int(ysize))] for col in range(int(xsize))]
    for x in range(int(xmin),int(xmax)):
        for y in range(int(ymin),int(ymax)):
            P = (x,y)
            for segment in allSegments:
                dist = SD.point_segment_distance(P,segment)
                if dist <= tolerance:
                    P2 = convertCoordToGrid(P,limits)
#                    print P2
                    grid[int(P2[0])][int(P2[1])] = 1
                    break
    print "Making the grid took",time.time()-startTime,"seconds"
    return grid
    
def makeGridv2(limits,platformSegs,wallSegsNoPlat,tolerance=tol):
    startTime = time.time()
    xmin,xmax,ymin,ymax = limits
    xsize = xmax-xmin
    ysize = ymax-ymin
    grid1 = [[0 for row in range(int(ysize))] for col in range(int(xsize))]
    grid2 = [[0 for row in range(int(ysize))] for col in range(int(xsize))]
    for x in range(int(xmin),int(xmax)):
        for y in range(int(ymin),int(ymax)):
            P = (x,y)
            P2 = convertCoordToGrid(P,limits)
            for segment in wallSegsNoPlat:
                dist = SD.point_segment_distance(P,segment)
                if dist <= tolerance:
                    grid1[int(P2[0])][int(P2[1])] = 1
                    grid2[int(P2[0])][int(P2[1])] = 1
                    break
            if grid1[int(P2[0])][int(P2[1])] == 0:
                for segment in platformSegs:
                    dist = SD.point_segment_distance(P,segment)
                    if dist <= tolerance:
                        grid1[int(P2[0])][int(P2[1])] = 1
                        break
                
    print "Making the grid took",time.time()-startTime,"seconds"
    return grid1,grid2  
    
def getDesiredAngle(P1,P2):
    x,y = P2.getX()-P1.getX(),P2.getY()-P1.getY()
#    print "x,y:",x,y
    if y==0 and x==0:
        angle = 0.
    elif y==0:
        if x>0:
            angle = 0.
        else:
            angle = math.pi
    elif x==0:
        if y>0:
            angle = math.pi/2
        else:
            angle = 3*math.pi/2
    else:
        angle = math.atan(y/x)
        if x<0:
            angle += math.pi
#    print "desired angle:",math.degrees(angle)
    return angle
  
def main(fileName):
    win,bounds,allWalls,allPlats,allSegments,wallSegsNoPlat,platformSegs,allBlocks,robot,robotCenter = initializeWindow(fileName)
#    grid = makeGrid(bounds, allSegments)
#    grid2 = makeGrid(bounds, wallSegsNoPlat)
    grid,grid2 = makeGridv2(bounds,platformSegs,wallSegsNoPlat)
    allBoundries = allWalls + allPlats
    currentTheta = math.pi/2
    deltaX = 1
    dt = .1/5
    while len(allBlocks)>0:
        chosenBlock,finalPath = getPath(win,grid,bounds,allBoundries,allSegments,allBlocks,robot,robotCenter)
        for i in range(len(finalPath)-1):
            desiredAngle = getDesiredAngle(robotCenter,finalPath[i+1])
            robot = rotateRobot(robot,robotCenter,desiredAngle-currentTheta,win)
            currentTheta = desiredAngle
            lastTimeMove = time.time()
            while calculatHeuristic((robotCenter.getX(),robotCenter.getY()),(finalPath[i+1].getX(),finalPath[i+1].getY()))>2:
                if time.time()-lastTimeMove>dt:
                    lastTimeMove = time.time()
                    moveRobot(robot,robotCenter,deltaX,currentTheta,win)
        chosenBlock.undraw()
        allBlocks.remove(chosenBlock)
#        print "--------------.------------"
    print "all blocks collected"
    chosenPlat,finalPath = getPath(win,grid2,bounds,allBoundries,wallSegsNoPlat,allPlats,robot,robotCenter)
    print "going for platform"
    for i in range(len(finalPath)-1):
        desiredAngle = getDesiredAngle(robotCenter,finalPath[i+1])
#        print "current theta:",math.degrees(currentTheta),"desired theta:",math.degrees(desiredAngle)
        robot = rotateRobot(robot,robotCenter,desiredAngle-currentTheta,win)
        currentTheta = desiredAngle
        lastTimeMove = time.time()
        while calculatHeuristic((robotCenter.getX(),robotCenter.getY()),(finalPath[i+1].getX(),finalPath[i+1].getY()))>2:
            if time.time()-lastTimeMove>dt:
                lastTimeMove = time.time()
                moveRobot(robot,robotCenter,deltaX,currentTheta,win)
        
    win.close()

main(file1)
main(file2)
main(file3)
main(file4)
main(file5)