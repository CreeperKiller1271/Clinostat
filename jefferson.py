import time
import random
from simple_pid import PID

class accell:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.z = -1
        self.m1dir = False
        self.m2dir = False
        self.m1S = 20
        self.m2S = 20

    #resolution is 0.01sec
    def step(self, m1adj, m2adj):
        #moves on m1 assuming full speed is 20rpm
        if(self.m1dir == False):
            self.x += (40/6000)*m1adj
            if(self.x >= 1):
                self.x = -1
        if(self.m1dir == True):
            self.x -= (40/6000)*m1adj
            if(self.x <= -1):
                self.x = 1                     
        #moves on m2 assuming full speed is 20rpm
        if(self.m2dir == False):
            self.y += (40/6000)*m2adj
            if(self.y >= 1):
                self.y = -1
        if(self.m2dir == True):
            self.y -= (40/6000)*m2adj
            if(self.y <= -1):
                self.y = 1             
        #deels with the complicated z axis        
        






startTime = time.time() # finds the start time
dev = accell()
while(True):
    dev.step(1, 1)
    print("x: ", '{0:.2f}'.format(dev.x), " y: ", '{0:.2f}'.format(dev.y), " z: ", '{0:.2f}'.format(dev.z))
    time.sleep(0.1)