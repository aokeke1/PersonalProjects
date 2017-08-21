from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Encoder, Gyro, Motor, AnalogInput, Color, Servo
import numpy as np
import cv2
import math
from graphics import *

#Wall follow with the wall on the left of the robot until it sees a block.
#Does not yet incorporate a pause and rotate during wall following.
#When it sees a block, it stops wall following and goes to pick it up.

class DriveStraight(SyncedSketch):
    #motor pins
    left_motor_dir_pin, left_motor_pwm_pin = 2,3
    right_motor_dir_pin, right_motor_pwm_pin = 4,5
    #encoder pins
    left_motor_encoder_pins = 6, 7
    right_motor_encoder_pins = 8, 9
    #gyroscope pin
    ss_pin = 10
    
    #set the initial motor speeds for drive wheels, block positioner, and elevator
    init_motor_speed = 50
    
    #Initial values for calculating estimated theta
    desired_theta = 0.0
    theta_gyro_old = 0.0
    theta_est = 0.0
    #physical constants for using encoder to estimate theta
    left_motor_encoder_old = 0.0
    right_motor_encoder_old = 0.0
    axel_length = 11 #distance between two wheels
    wheel_radius = 1.435 #radius of wheels
    wheel_circumference = 2*wheel_radius*np.pi
    counts_per_rotation = 3200.0 #from the motor ecoder specs
    #using encoder to calculate distance travelled when block collecting
    left_motor_encoder_old2 = 0.0
    right_motor_encoder_old2 = 0.0
    left_desired_encoder = 0.0
    right_desired_encoder = 0.0
    bias = 0.0
    power = 0.0
    extra = 2000 #extra encoder rotation so block actually gets in
    #Values for PID calculations
    last_diff = 0.0
    integral = 0.0
    derivative = 0.0
    dt = 0.0
    alpha = 0.9
    kP = 2
    kI = 1e-3
    kD = 110
    largeAngle = 20
    maxTurnSpeed = 50

    #How often to perform calculations in milliseconds
    refresh_rate = 10

    #Parameters for webcam
    webcamNumber = -1
    webcamWidth = 160
    webcamHeight = 120
    CAMERA_CENTER = (webcamWidth/2,webcamHeight/2)
    #For when rotating without block in site
    deltaTheta = 2
    

    #Overall robot state    
    state = 0    
    
    #Calculate location
    initialPos1 = (0,0,0) #x,y,theta
    left_encoder_prev1 = 0
    right_encoder_prev1 = 0
    
    initialPos2 = (0,0,0) #x,y,theta
    left_encoder_prev2 = 0
    right_encoder_prev2 = 0
    

    #Target
    targets = [(0,0,0),(12,0,90),(12,12,180),(0,12,270)]
    target = targets[0]
    driveToTargetState = 0
    straightCount = 0
    part1=True
    
    
    def setup(self):
        
        #set up timer
        self.timer = Timer()
        self.timer2 = Timer()
        self.timer3 = Timer()
        
        #set up motors
        self.left_motor = Motor(self.tamp, self.left_motor_dir_pin, self.left_motor_pwm_pin)
        self.right_motor = Motor(self.tamp, self.right_motor_dir_pin, self.right_motor_pwm_pin)
        self.motorval_left = 0
        self.motorval_right = 0
        print "drive motor objects made"
        
        #set up encoders
        self.left_motor_encoder = Encoder(self.tamp, *self.left_motor_encoder_pins, continuous=True)
        self.right_motor_encoder = Encoder(self.tamp, *self.right_motor_encoder_pins, continuous=True)
        print "encoder objects made"

        #set up the gyro
        self.gyro = Gyro(self.tamp, self.ss_pin, integrate=True)
        print "gyro object made"

        #set up the webcam
#        self.cap = cv2.VideoCapture(self.webcamNumber)
#        self.cap.set(3,self.webcamWidth)
#        self.cap.set(4,self.webcamHeight)

        #start all motors
        self.left_motor.write(self.motorval_left<0, abs(self.motorval_left))
        self.right_motor.write(self.motorval_right<0, abs(self.motorval_right))
        
        #set up the visualization
        self.win = GraphWin('RobotTracking', 500, 500)
        self.win.setCoords(0, 0, 500, 500)
        start = (self.initialPos2[0],self.initialPos2[1])
        delta = 5.0
        corners = [Point(start[0]+delta,start[1]),Point(start[0]-delta,start[1]-delta/2),Point(start[0]-delta,start[1]+delta/2)]
        self.robot = Polygon(*corners)
        self.robot.setFill('red')
        self.robot.draw(self.win)
        self.robotCenter = Point(start[0],start[1])
        self.robotCenter.setFill('white')
        self.robotCenter.draw(self.win)
        self.rotateRobot(self.initialPos2[2])

    def loop(self):
        if self.timer3.millis()<175*1000:
            if self.timer.millis() > self.refresh_rate:
                self.dt = self.timer.millis()
                self.timer.reset()
#                _,frame = self.cap.read()
#                self.updateThetaEstNoEncoder()
#                self.calculatePower()
#                if self.last_diff<.5:
#                    self.bias=25
#                else:
#                    self.bias=0
#                if self.initialPos1[0]>=12:
#                    self.desired_theta = -90.
#                if self.initialPos1[1]>=12:
#                    self.bias = 0
#                self.updateMotors()
                if self.part1==True:
                    self.target=(60,24,90)
#                    self.target=(0,0,90)
                if self.state == 0:
                    result = self.driveToTarget()
                    if result:
                        self.part1=False
                        if self.target==(0,0,0):                            
                            self.state=-1
                            self.win.close()
                        else:
                            self.target=(0,0,0)
#                        try:
#                            self.target=self.targets[self.targets.index(self.target)+1]
#                        except:
#                            self.target = self.targets[0]
#                elif self.state == 1:
#                    self.pickUpBlock()
                    
                #Print status
                print "overall state:",self.state
                print "driveToTarget state:",self.driveToTargetState,"straightCount:",self.straightCount
                print "target:",self.target
                #Update and print positions
                self.updateAllPos()
                print "theta_est:",self.theta_est,"desired_theta:",self.desired_theta
                print "visual position:",self.robotCenter.getX(),self.robotCenter.getY()
                #print "power:",self.power, ", gyro:",self.gyro.val, ", theta_est:", self.theta_est
                #print "last_diff",self.last_diff,"dt:",self.dt, "desired_theta", self.desired_theta
                #print "integration:", self.integral, "derivative:",self.derivative
                #print other stuff
                print "left motor:",self.motorval_left,"right motor",self.motorval_right
                print "bias:",self.bias
                print "left encoder:",self.left_motor_encoder.val,"right encoder:", self.right_motor_encoder.val
                print "left desired:", self.left_desired_encoder,"right desired:", self.right_desired_encoder
                
                print "------------------.---------"
	else:
		#start all motors
		self.left_motor.write(self.motorval_left<0, 0)
		self.right_motor.write(self.motorval_right<0, 0)

    def driveToTarget(self):
        self.updateThetaEstNoEncoder()
        #get direction and set bias to 0 until we are at the correct angle
        currState = self.initialPos2
        P1 = (currState[0],currState[1])
        P2 = (self.target[0],self.target[1])

        if self.driveToTargetState==0:
            #turn toward the point and drive
            angle = -math.degrees(self.getDesiredAngle(P1,P2))
            angle = self.getClosestEquivalentAngle(angle)
            print "angle:",angle
            print "deltaTheta:",abs(self.theta_est - angle)
            #don't drive unless we are pointing in the correct direction
            if abs(self.theta_est - angle) <= 10:
                self.driveToTargetState=1
                
            if self.theta_est<angle:
                self.desired_theta = self.theta_est + 5
            elif self.theta_est>angle:
                self.desired_theta = self.theta_est - 5
                    
#            self.desired_theta = -math.degrees(angle)
            self.bias = 0

        elif self.driveToTargetState==1:
            angle = -math.degrees(self.getDesiredAngle(P1,P2))
            angle = self.getClosestEquivalentAngle(angle)
            print "angle:",angle
            print "deltaTheta:",abs(self.theta_est - angle)
            self.desired_theta = angle
            self.bias = self.init_motor_speed
            #switch states if we are within 1 inch of our goal
            if math.hypot(P2[0]-P1[0], P2[1]-P1[1])<=1:
                self.driveToTargetState = 2
                self.bias = 0
        elif self.driveToTargetState==2:
            if type(self.target[2])==float or type(self.target[2])==int:
                angle = -self.target[2]
            else:
                angle = self.theta_est
            angle = self.getClosestEquivalentAngle(angle)
            print "angle:",angle
            print "deltaTheta:",abs(self.theta_est - angle)
            #print in the direction specified in the target
#            self.desired_theta = -self.target[2]
            self.bias = 0
            if abs(self.theta_est - angle) < 10:
                self.desired_theta = angle
                if abs(self.desired_theta-self.theta_est)<3:
                    self.straightCount += 1
                elif abs(self.desired_theta-self.theta_est)>=3:
                    self.straightCount = 0
                if self.straightCount == 10:
                    self.desired_theta = self.theta_est
#                    self.calculatePower()
                    self.power = 0
                    self.updateMotors()
                    self.driveToTargetState = 0
                    self.straightCount = 0
                    return True
            else:
                if self.theta_est<angle:
                    self.desired_theta = self.theta_est + 10
                elif self.theta_est>angle:
                    self.desired_theta = self.theta_est - 10        
        self.calculatePower()
        self.updateMotors()
        return False

    def getClosestEquivalentAngle(self,angle):
        #takes an angle and uses robots current position to determine which angle to turn 
        pa = self.theta_est - (self.theta_est%360 - angle%360)
        
        potentialAngles = [pa-360,pa,pa+360]
        differences = [abs(self.theta_est - potentialAngles[0]), abs(self.theta_est - potentialAngles[1]), abs(self.theta_est - potentialAngles[2])]
        return potentialAngles[differences.index(min(differences))]

    def getDesiredAngle(self,P1,P2):
        x,y = P2[0]-P1[0],P2[1]-P1[1]
        print "x,y:",x,y
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
        return angle

    def updateAllPos(self):
        self.updateInitPos1()
        self.updateInitPos2()
        print "version 1:",self.initialPos1
        print "version 2:",self.initialPos2
        
    def updateInitPos1(self):
        #assume we went in a straight line at every time step in the direction of theta
        
        deltaLeft = self.wheel_circumference*((self.left_motor_encoder.val - self.left_encoder_prev1)/self.counts_per_rotation) #number of rotations*circumference
        deltaRight = self.wheel_circumference*((self.right_motor_encoder.val - self.right_encoder_prev1)/self.counts_per_rotation) #number of rotations*circumference
        dist = (deltaLeft+deltaRight)/2.0
        angle = math.radians(self.initialPos1[2])
        self.updateThetaEstNoEncoder()
        self.initialPos1 = (self.initialPos1[0] + dist*math.cos(angle),self.initialPos1[1] + dist*math.sin(angle),-self.theta_est)
        
        self.left_encoder_prev1 = self.left_motor_encoder.val
        self.right_encoder_prev1 = self.right_motor_encoder.val
        
    def rotateRobot(self,deltaTheta):
        #rotates a triangle a certain deltaTheta radians
        #???
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

    def updateInitPos2(self):
        #using equations for differential steering, but replacing the angle with the value from the gyroscope
        #http://robotics.stackexchange.com/questions/1653/calculate-position-of-differential-drive-robot
        self.updateThetaEstNoEncoder()
        x = self.initialPos2[0]
        y = self.initialPos2[1]
        heading = math.radians(self.initialPos2[2])
        
        leftEnc = self.left_motor_encoder.val
        rightEnc = self.right_motor_encoder.val
        
        leftDelta = float(self.wheel_circumference)*((leftEnc - self.left_encoder_prev2)/self.counts_per_rotation) #number of rotations*circumference
        rightDelta = float(self.wheel_circumference)*((rightEnc - self.right_encoder_prev2)/self.counts_per_rotation) #number of rotations*circumference
        if abs(leftDelta-rightDelta)<=1e-6:
            new_x = x + leftDelta*math.cos(heading)
            new_y = y + rightDelta*math.sin(heading)
            
        else:
            R = self.axel_length*(leftDelta+rightDelta)/(2.0*(rightDelta-leftDelta))
            wd = (rightDelta-leftDelta)/self.axel_length
            
            new_x = x + R * math.sin(wd + heading) - R * math.sin(heading)
            new_y = y - R * math.cos(wd + heading) + R * math.cos(heading)

        new_heading = -self.theta_est
        self.initialPos2 = (new_x,new_y,new_heading)

        dx = (self.initialPos2[0] - self.robotCenter.getX())
        dy = (self.initialPos2[1] - self.robotCenter.getY())
        startPoint  = self.robotCenter.clone()
        self.robot.move(dx,dy)
        self.robotCenter.move(dx,dy)
        deltaTheta = math.radians(self.initialPos2[2]) - heading
        self.rotateRobot(deltaTheta)
        endPoint  = self.robotCenter.clone()
        trail = Line(startPoint,endPoint) # set endpoints
        trail.setWidth(1)
        trail.setFill('blue')
        trail.draw(self.win)           
        
        self.left_encoder_prev2 = leftEnc
        self.right_encoder_prev2 = rightEnc
    
    def getAngles(self):
        left_arc = self.wheel_circumference*(self.left_motor_encoder.val/self.counts_per_rotation) #number of rotations*circumference
        right_arc = self.wheel_circumference*(self.right_motor_encoder.val/self.counts_per_rotation) #number of rotations*circumference
        angleEnc = math.degrees(((left_arc - right_arc)/self.axel_length)) #converted to degrees
        print "angle from encoders:",angleEnc
        print "angle from gyro:",self.gyro.val
        
        
    def updateThetaEstNoEncoder(self):
        #Only use gyroscope to estimate current angle
        self.theta_est = self.gyro.val - self.initialPos2[2]

    def calculatePower(self):
        #Use PID and update motors
        diff = self.desired_theta - self.theta_est
        self.integral = self.integral + diff*self.dt
        self.derivative = (diff - self.last_diff)/self.dt
        self.power = self.kP*diff + self.kI*self.integral + self.kD*self.derivative
        self.last_diff = diff

    def updateMotors(self):
        #Prevent a power that will try to set the wheels above or below possible values
        if ((self.bias + self.power)>255) or ((self.bias - self.power)<-255):
            self.power = 255 - abs(self.bias)
        elif ((self.bias + self.power)<-255) or ((self.bias - self.power)>255):
            self.power = -255 + abs(self.bias)
            
        #Stop power from being too high so the change in wheel speed is not too drastic
        if self.power>self.maxTurnSpeed:
            self.power = self.maxTurnSpeed
        elif self.power<-self.maxTurnSpeed:
            self.power = -self.maxTurnSpeed
            
        #Set motor values
        self.motorval_left = self.bias + self.power
        self.motorval_right = self.bias - self.power
        self.left_motor.write(self.motorval_left<0, abs(self.motorval_left))
        self.right_motor.write(self.motorval_right<0, abs(self.motorval_right))
            
    def encodersAboveDesired(self):
        #Returns true if the sum of the encoder values are greater than or equal to the sum of the desired values.
        #True if you are in front of or at where you wanted to travel.
        return self.left_motor_encoder.val+self.right_motor_encoder.val>=self.left_desired_encoder+self.right_desired_encoder


    def getDistTravelled(self,oldLeftEnc,oldRightEnc,newLeftEnc,newRightEnc):
        return self.wheel_circumference*((newLeftEnc+newRightEnc)-(oldLeftEnc+oldRightEnc))/3200.0

        
if __name__ == "__main__":
    sketch = DriveStraight(1, -0.00001, 100)
    sketch.run()
