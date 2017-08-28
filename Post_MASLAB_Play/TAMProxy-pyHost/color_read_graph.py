from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Color
import color_readfunc
import matplotlib.pyplot as plt
import numpy as np
# Prints RGB, clear(C), colorTemp, and lux values read and
# computed from the device. For more details, see the Adafruit_TCS34725
# Arduino library, from which the colorTemp and lux computations are
# used.

# Color sensor should be connected to the I2C ports (SDA and SCL)

class ColorRead(SyncedSketch):
    resultsR = []
    resultsG = []
    resultsB = []
    resultsC = []
    resultsT = []
    resultsL = []
    def setup(self):
        color_readfunc.init()
        self.color = Color(self.tamp,
                           integrationTime=Color.INTEGRATION_TIME_101MS,
                           gain=Color.GAIN_1X)
        self.timer = Timer()
        self.timer2 = Timer()

    def loop(self):
#        if self.timer2.millis()>1000*5:
##            xvals = [self.resultsR,self.resultsG,self.resultsB,self.resultsC,self.resultsT,self.resultsL]
#            labels = ["Red","Blue"]
#            xvals = [self.resultsR,self.resultsB,self.resultsC,self.resultsT,self.resultsL]
#            y = self.resultsG
##            color = ["ro",'go','bo']
##            for i in range(3):
##                x = xvals[i]
##                label = labels[i]
##                plt.plot(range(len(x)),x,color[i],label = label[i])
#            for i in range(2):
##                sub = plt.subplot(1, 6, i+1)
#                label = labels[i]
#                x = xvals[i]
#                fit = np.polyfit(x,y,1)
#                fit_fn = np.poly1d(fit) 
#                # fit_fn is now a function which takes in x and returns an estimate for y
#                plt.plot(x,y, 'yo', x, fit_fn(x), '--k')
#                plt.xlim(min(x), max(x))
#                plt.ylim(min(y), max(y))
#                plt.xlabel(label)
#                plt.ylabel('Red')
#                print "Red =",fit[0],"*",label,"+",fit[1]
#                plt.show()
#            raise KeyboardInterrupt
##            pause = raw_input("pause")
#        else:
        if self.timer.millis() > 100:
            self.timer.reset()
#            print self.color.r, self.color.g, self.color.b, self.color.c
#            print self.color.colorTemp, self.color.lux
#            self.resultsR.append(self.color.r)
#            self.resultsG.append(self.color.g)
#            self.resultsB.append(self.color.b)
#            self.resultsC.append(self.color.c)
#            self.resultsT.append(self.color.colorTemp)
#            self.resultsL.append(self.color.lux)
            if self.color.r>1.06*self.color.g and self.color.r>1.0*self.color.b:
                print "Red Ball"
            elif self.color.g>1.08*self.color.r and self.color.g>1.0*self.color.b:
                print "Green Ball"
            else:
                try:
                    print "r/g",float(self.color.r)/self.color.g
                    print "r/b",float(self.color.r)/self.color.b
                    print "g/r",float(self.color.g)/self.color.r
                    print "g/b",float(self.color.g)/self.color.b
                except:
                    print "None"
            print "----------------------.---------------------"

if __name__ == "__main__":
    sketch = ColorRead(1, -0.00001, 100)
    sketch.run()
