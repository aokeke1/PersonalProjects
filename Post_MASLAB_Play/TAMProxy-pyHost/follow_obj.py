
from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Motor,Encoder
import PinSettings as PS
import numpy as np
import math
import cv2
import math
from graphics import *
import copy

# Cycles a motor back and forth between -255 and 255 PWM every ~5 seconds

class Drive(Sketch):

    def setup(self):
        self.motors = (Motor(self.tamp, *PS.left_motor_pins),Motor(self.tamp, *PS.right_motor_pins)) #(L,R)
        self.motors[0].write(1,0)
        self.motors[1].write(1,0)
        self.motorvals = (0,0) #(L,R)
        
        #PID
        self.bias = 0
        self.power = 0
        self.desired_theta = 0
        self.dt = 0
        self.integral = 0
        self.last_diff = 0
        self.derivative = 0
        self.maxTurnSpeed = PS.maxTurnSpeed
        self.largeAngle = PS.largeAngle
        self.kP = PS.kP
        self.kI = PS.kI
        self.kD = PS.kD

        
        #Encoders
        self.encoders = (Encoder(self.tamp, *PS.left_encoder_pins, continuous=True),Encoder(self.tamp, *PS.right_encoder_pins, continuous=True)) #(L,R)
        self.prev_encoder = (0,0) #(L,R)
        self.pos = (0,0,0) #(x,y,angle [deg])        
        
        #Timers
        self.timer = Timer()
        self.full_timer = Timer()
        self.status_timer = Timer()
        
        #Load settings
        self.counts_per_rotation = PS.counts_per_rotation
        self.axel_length = PS.axel_length
        self.wheel_circumference = PS.wheel_circumference

        #set up the visualization
        self.win = GraphWin('RobotTracking', 500, 500)
        self.win.setCoords(0, 0, 500, 500)
        delta = 5.0
        corners = [Point(self.pos[0]+delta,self.pos[1]),Point(self.pos[0]-delta,self.pos[1]-delta/2),Point(self.pos[0]-delta,self.pos[1]+delta/2)]
        self.robot = Polygon(*corners)
        self.robot.setFill('red')
        self.robot.draw(self.win)
        self.robotCenter = Point(self.pos[0],self.pos[1])
        self.robotCenter.setFill('white')
        self.robotCenter.draw(self.win)
        self.rotateRobotGraphic(self.pos[2])        
        
        #For driving to a coordinate
#        self.targets = [(24,0,None),(24,24,None),(0,24,None),(0,0,None)]
#        self.targInd = 0
        
        #set up the webcam
        self.webcamWidth = PS.webcamWidth 
        self.webcamHeight = PS.webcamHeight
        self.CAMERA_CENTER = PS.CAMERA_CENTER
        self.maxDriveSpeed = PS.maxDriveSpeed
        self.cap = cv2.VideoCapture(PS.webcamNumber)
        self.cap.set(3,self.webcamWidth)
        self.cap.set(4,self.webcamHeight)
        
        #Image Processing Variables
        self.rg=PS.rg
        self.rb=PS.rb
        self.gr=PS.gr
        self.gb=PS.gb
        self.obj_cascade = PS.obj_cascade
        #Block tracking
        self.targetLocked = False

    def loop(self):
        #drive for two seconds
        if self.full_timer.millis()/1000<100:
            if (self.timer.millis() > 10):
                self.dt = self.timer.millis()
                self.timer.reset()
                #Dead reckoning
                deltaPos = self.updatePos()
                self.updateGraphic(deltaPos)
                
                self.ret,self.frame = self.cap.read()
                
                self.trackObjs()
                self.displayCamera()

                #Driving to specific coordinates
#                desiredPos = self.targets[self.targInd%len(self.targets)]
#                self.targInd += self.driveToPos(desiredPos)
                self.calculatePower()
                self.updateMotors()
                
            if self.status_timer.millis()>500:
                self.status_timer.reset()
                self.printStatus()
        #quit
        else:
            self.motorvals = (0,0)
            self.motors[0].write(1,0)
            self.motors[1].write(1,0)
            print ("done!")
            raise KeyboardInterrupt
          
    def trackObjs(self):
        if self.ret:
            self.frame2 = copy.copy(self.frame)

            gray = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2GRAY)
            objs = self.obj_cascade.detectMultiScale(gray, 1.3, 5)
            for (ex,ey,ew,eh) in objs:
                cv2.rectangle(self.frame2,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

            self.sorted_objs = self.sort_objs(objs)
            self.targetLocked = False
            if len(self.sorted_objs)==0:
                self.bias = 0
                self.desired_theta = self.pos[2]
                self.last_diff = 0.0
                self.integral = 0.0
                self.derivative = 0.0
            else:
#                print ("obj seen")
#                print (self.sorted_objs,self.sorted_objs[0],type(self.sorted_objs),type(self.sorted_objs[0]))
                (ex,ey,ew,eh) = self.sorted_objs[0]
                cv2.rectangle(self.frame2,(ex,ey),(ex+ew,ey+eh),(255,255,0),2)
                
                cx = int(ex + ew/2.0)
                cy = int(ey + eh/2.0)
                
                self.targetLocked = True
                offsetX = (30.0/self.webcamWidth)*(self.CAMERA_CENTER[0]-cx)
                self.desired_theta = self.pos[2] + offsetX
                trackConst = 0.5
                offsetY = self.CAMERA_CENTER[1]-cy
                self.bias = offsetY*trackConst
            
        
    def filter_contours(self,frame,height,width,ratio = 0.01):
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
    def sort_objs(self,objs):
        areas = []
        indeces = []
        i=0
        for (ex,ey,ew,eh) in objs:
            areas.append(ew*eh)
            indeces.append(i)
            i+=1
        sortedIndeces = [x for _,x in sorted(zip(areas,indeces))]
        sortedObjs = []
        for i in sortedIndeces:
            sortedObjs.append(objs[i])
        return sortedObjs
    def displayCamera(self):
        if self.ret:
#            cv2.imshow("Original", self.frame)
            cv2.imshow("Filtered", self.frame2)
            cv2.waitKey(1)
#            if cv2.waitKey(1) & 0xFF == ord('q'):
#                break
    def updatePos(self):
        #using equations for differential steering, but replacing the angle with the value from the gyroscope
        #http://robotics.stackexchange.com/questions/1653/calculate-position-of-differential-drive-robot

        x,y,theta = self.pos
        heading = math.radians(self.pos[2])
        
        leftEnc = self.encoders[0].val
        rightEnc = self.encoders[1].val
        
        leftDelta = float(self.wheel_circumference)*(float(leftEnc - self.prev_encoder[0])/self.counts_per_rotation) #number of rotations*circumference
        rightDelta = float(self.wheel_circumference)*(float(rightEnc - self.prev_encoder[1])/self.counts_per_rotation) #number of rotations*circumference
        
        if abs(leftDelta-rightDelta)<=1e-6:
            dx = leftDelta*math.cos(heading)
            dy = rightDelta*math.sin(heading)
            wd = 0
            
        else:
            R = self.axel_length*(leftDelta+rightDelta)/(2.0*(rightDelta-leftDelta))
            wd = (rightDelta-leftDelta)/self.axel_length

            dx = R * math.sin(wd + heading) - R * math.sin(heading)
            dy =  - R * math.cos(wd + heading) + R * math.cos(heading)           
            

        dTheta = wd
#        print (dx,dy,dTheta,math.degrees(dTheta),leftEnc,rightEnc,self.prev_encoder[0],self.prev_encoder[1])
        self.pos = (x+dx,y+dy,theta+math.degrees(dTheta))
        
        self.prev_encoder = (leftEnc,rightEnc)
        deltaPos = (dx,dy,dTheta)
        return deltaPos
    
    def updateAll(self):
        _,frame = self.cap.read()
        deltaPos = self.updatePos()
        self.updateGraphic(deltaPos)
        self.calculatePower()
        self.updateMotors()
        
    def updateGraphic(self,deltaPos):
        #dTheta is in radians
        dx,dy,dTheta = deltaPos
        
        #Move the robot
        startPoint  = self.robotCenter.clone()
        self.robot.move(dx,dy)
        self.robotCenter.move(dx,dy)
        
        #Rotate
        self.rotateRobotGraphic(dTheta)
        
        #Draw the trail
        endPoint  = self.robotCenter.clone()
        trail = Line(startPoint,endPoint) # set endpoints
        trail.setWidth(1)
        trail.setFill('blue')
        trail.draw(self.win)

    def rotateRobotGraphic(self,deltaTheta):
        #rotates a triangle a certain deltaTheta radians
        points = self.robot.getPoints()
        newPoints = []
        for point in points:
            x2 = self.robotCenter.getX() + (point.getX() - self.robotCenter.getX())*math.cos(deltaTheta) - (point.getY() - self.robotCenter.getY())*math.sin(deltaTheta)
            y2 = self.robotCenter.getY() + (point.getY() - self.robotCenter.getY())*math.cos(deltaTheta) + (point.getX() - self.robotCenter.getX())*math.sin(deltaTheta)
            newPoints.append(Point(x2,y2))
        self.robot.undraw()
        self.robotCenter.undraw()
        robot = Polygon(*newPoints)
        robot.setFill('red')
        robot.draw(self.win)
        self.robotCenter.draw(self.win)
        self.robot = robot
        
    def getClosestEquivalentAngle(self,angle):
        #takes an angle and uses robots current position to determine which angle to turn 
        pa = self.pos[2] - (self.self.pos[2]%360 - angle%360)
        
        potentialAngles = [pa-360,pa,pa+360]
        differences = [abs(self.pos[2] - potentialAngles[0]), abs(self.pos[2] - potentialAngles[1]), abs(self.pos[2] - potentialAngles[2])]
        return potentialAngles[differences.index(min(differences))]

    def getDesiredAngle(self,P1,P2):
        x,y = P2[0]-P1[0],P2[1]-P1[1]
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
#        print "desired angle:",math.degrees(angle)
        return math.degrees(angle)
        
    def getDistance(self,P1,P2):
        return math.sqrt(((P1[0]-P2[0])**2)+((P1[1]-P2[1])**2))
        
    def driveToPos(self,desiredPos):
        errorDistAllowed = 5 #inches
        errorAngleAllowed = 10 #degrees
        if self.getDistance(self.pos,desiredPos)<errorDistAllowed:
            #reached the desired location. rotate to desired angle
            if desiredPos[2] is None:
                return True
            self.bias = 0
            if abs(self.pos[2]-desiredPos[2])<errorAngleAllowed:
                return True
            else:
                self.desired_theta = desiredPos[2]
                return False
        else:
            #drive toward the target
            self.desired_theta = self.getDesiredAngle(self.pos,desiredPos)
            if abs(self.pos[2]-self.desired_theta)<self.largeAngle:
                self.bias = 50
            else:
                self.bias = 0
        return False
                
    def calculatePower(self):
        #Use PID and update motors
        diff = self.desired_theta - self.pos[2]
        self.integral = self.integral + diff*self.dt
        self.derivative = (diff - self.last_diff)/self.dt
        self.power = self.kP*diff + self.kI*self.integral + self.kD*self.derivative
        self.last_diff = diff
        
    def updateMotors(self):
        #Prevent a power that will try to set the wheels above or below possible values
        if ((self.bias + self.power)>self.maxDriveSpeed) or ((self.bias - self.power)<-self.maxDriveSpeed):
            self.power = self.maxDriveSpeed - abs(self.bias)
        elif ((self.bias + self.power)<-self.maxDriveSpeed) or ((self.bias - self.power)>self.maxDriveSpeed):
            self.power = -self.maxDriveSpeed + abs(self.bias)
            
        #Stop power from being too high so the change in wheel speed is not too drastic
        if self.power>self.maxTurnSpeed:
            self.power = self.maxTurnSpeed
        elif self.power<-self.maxTurnSpeed:
            self.power = -self.maxTurnSpeed
            
        #Set motor values
        self.motorvals = self.bias - self.power,self.bias + self.power
        self.motors[0].write(self.motorvals[0]<0, abs(self.motorvals[0]))
        self.motors[1].write(self.motorvals[1]<0, abs(self.motorvals[1]))

    def printStatus(self):
        print ("--------------------------")
        print ("bias:",self.bias,"power:",self.power)
        print ("last_diff:",self.last_diff*self.kP,"integral:",self.integral*self.kI,"derivative:",self.derivative*self.kD)
        print ("pos:",self.pos)
#        print ("desiredPos",self.targets[self.targInd%len(self.targets)])
        print ("desired angle:",self.desired_theta)
        print ("Target locked:",self.targetLocked)
        print ("--------------------------")
        
if __name__ == "__main__":
    sketch = Drive()
    sketch.run()
    try:
        pause = raw_input("Press enter to close the window.")
    except:
        sketch.win.close()
        sketch.cap.release()
        cv2.destroyAllWindows()
    sketch.win.close()
    sketch.cap.release()
    cv2.destroyAllWindows()