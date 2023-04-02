import time
import random
from simple_pid import PID
import math
import datetime

class accell:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.z = -1
        self.m1dir = 1
        self.m2dir = 1
        self.m1step = 0
        self.m2step = 0
        self.stepSize = 0.1

    #resolution is 0.01sec
    def step(self, m1adj, m2adj):
        #moves on m1 assuming full speed is 10rpm
        self.m1step += self.m1dir*self.stepSize
        self.y = math.sin(m1adj*(10/60)*2*math.pi*self.m1step)
        self.m2step += self.m2dir*self.stepSize
        self.x = (1-abs(self.x))*math.sin(m2adj*(30/60)*2*math.pi*self.m2step)

        self.z = math.cos(m1adj*(10/60)*2*math.pi*self.m1step)*((1-abs(self.y))*math.cos(m2adj*(30/60)*2*math.pi*self.m2step))






startTime = time.time() # finds the start time
logFile = open('logs/{date:%Y-%m-%d_%H:%M:%S}.csv'.format( date=datetime.datetime.now() ), 'w')
logFile.write("Loop#, Current X, Current Y, Current Z, Average X, Average Y, Average Z, Gravity\n")

dev = accell()
xTot = 0
yTot = 0
zTot = 0

xAvg = 0
yAvg = 0
zAvg = 0
gAvg = 0

loopDirChange = 0

for loop in range(0,6000):
    dev.step(1, 0.9)
    xTot += dev.x
    yTot += dev.y
    zTot += dev.z
    
    xAvg = xTot/(loop+1)
    yAvg = yTot/(loop+1)
    zAvg = zTot/(loop+1)
    gAvg = math.sqrt((xAvg**2)+(yAvg**2)+(zAvg**2))
    logFile.write(f"{(loop+1)}, {dev.x}, {dev.y}, {dev.z}, {xAvg}, {yAvg}, {zAvg}, {gAvg}\n")

    if(loopDirChange > 30): #will attempt to change the direction every 3-30 seconds
        if(random.choice(range(0,2)) == 1): #1/5 chance motor 1 changes direction
            dev.m1dir = dev.m1dir * -1
        if(random.choice(range(0,2)) == 1): #1/5 chance motor 2 changes direction
            dev.m2dir = dev.m2dir * -1    
        loopDirChange = 0

    loopDirChange += 1

    #print("x: ", '{0:.2f}'.format(dev.x), " y: ", '{0:.2f}'.format(dev.y), " z: ", '{0:.2f}'.format(dev.z))