import time
from adafruit_motor import stepper
import random
from simple_pid import PID
from adafruit_motorkit import MotorKit
from FaBo9Axis_MPU9250 import MPU9250
import threading
from math import sqrt

#declares the motor kits at thier given adresses, This order should match the phyical order with hat 4 being closest to the pi and hat 1 being the top of the stack
hat1 = MotorKit(steppers_microsteps=128)
#hat2 = MotorKit(address=0x61)
#hat3 = MotorKit(address=0x62)
#hat4 = MotorKit(address=0x63)

#holds the values of the stepper so only the number needs passed to the function
stepDict = {
    #1: hat2.stepper1,
    #2: hat2.stepper2,
    #3: hat3.stepper1,
    #4: hat3.stepper2,
    #5: hat4.stepper1,
    #6: hat4.stepper2,
    #7: hat1.stepper1,   #Testing Only
    8: hat1.stepper2    #Testing Only
    }

#Contains all the information for the gravity system
class gravitySystem:

    def __init__(self):
        self.shutdown = False
        self.target = 0
        self.runTime = 30.0
        self.accelRom = MPU9250(address=0x68)
        self.minSpeed = .8 #motor speed to be used when homing the device
        self.maxSpeed = 1 #general motor speed before the algo adjusts it
        self.xAvg = 0
        self.yAvg = 0
        self.zAvg = 0 
        self.gAvg = 0

    def run(self):
        self.rThread = None
        self.rThread = threading.Thread(target=self.gravityRun)
        self.shutdown = False
        self.rThread.start()

    def stop(self):
        self.shutdown = True

    def setup(self, target: int, runTime: int):
        self.target = target
        self.runTime = runTime#*3600 #converts from hours to seconds

    def setSpeed(self, miSpeed: int, maSpeed: int):
        self.minSpeed = miSpeed
        self.maxSpeed = maSpeed

    #rotates the platform forward
    def rForward(self):
        hat1.motor2.throttle = self.minSpeed
        time.sleep(0.1)
        hat1.motor2.throttle = 0
        return

    #rotates the platform backward
    def rBackward(self):
        hat1.motor2.throttle = -self.minSpeed
        time.sleep(0.1)
        hat1.motor2.throttle = 0 
        return  

    #rotates the platform left
    def rLeft(self):
        hat1.motor1.throttle = self.minSpeed
        time.sleep(0.1)
        hat1.motor1.throttle = 0
        return

    #rotates the platform right
    def rRight(self):
        hat1.motor1.throttle = -self.minSpeed
        time.sleep(0.1)
        hat1.motor1.throttle = 0
        return

    def gravityRun(self):
        startTime = time.time() # finds the start time
        self.shutdown = False
        pid = PID(-1,-1,-1, setpoint=self.target, sample_time=.1)
        pid.output_limits = (self.minSpeed, self.maxSpeed)

        m1Speed = (self.maxSpeed+self.minSpeed)/2
        m2Speed = (self.maxSpeed+self.minSpeed)/2
        m1dir = 1   #allows for motor 1 to flip its direction
        m2dir = 1   #allows for motor 2 to flip its direction
        loop = 1    #keeps track of the current loop, needs to start at 1 for averaging
        loopDirChange = 1   #keeps track of the current loop for changing the direction
        xTot = 0    #totals the x accell over time
        yTot = 0    #totals the y accell over time
        zTot = 0    #totals the z accell over time
        self.xAvg = 0
        self.yAvg = 0
        self.zAvg = 0

        #main loop of the gravity system checks the 
        while (float(time.time() - startTime) < self.runTime )and self.shutdown == False:
            #sets the speeds of the motors for this loop]
            try:
                hat1.motor1.throttle = 1#m1Speed*m1dir
            except:
                pass
            try:
                hat1.motor2.throttle = .8#m2Speed*m2dir
            except:
                pass

            #gets the accelerometer values adds them to the total then calculates the rolling average.
            try:
                accel = self.accelRom.readAccel()
                xTot += abs(accel['x'])
                yTot += abs(accel['y'])
                zTot += abs(accel['z'])
                
                self.xAvg = xTot/loop
                self.yAvg = yTot/loop
                self.zAvg = zTot/loop
                self.gAvg = sqrt((self.xAvg**2)+(self.yAvg**2)+(self.zAvg**2))

                loop += 1
            except:
                #print("Unable to get data from accelerometer.")
                pass
            

            print("Gravity: ", '{0:.2f}'.format(self.gAvg))

            if(self.target != 0):
                m2Speed = pid(abs(self.zAvg))
                print("Adjusted Speed: ", m2Speed)

            if(loopDirChange > random.choice(range(30,300))): #will attempt to change the direction every 3-30 seconds
                if(random.choice(range(0,3)) == 1): #1/5 chance motor 1 changes direction
                    m1dir = m1dir * -1
                if(random.choice(range(0,3)) == 1): #1/5 chance motor 2 changes direction
                    m2dir = m2dir * -1    
                loopDirChange = 0

            loopDirChange += 1
            time.sleep(.1)  #loops every tenth of a second
        hat1.motor1.throttle = 0
        hat1.motor2.throttle = 0
        return


#class to hold the sequence for the mechanical loading
class stepperSequence:
    def __init__(self, rep) -> None:
        self.repeats = rep  #the number of times to repeat a given sequence
        self.steps = []     #an array to hold the sequence
        return

    #called from the UI to add a step to the sequence
    def addStep(self, step, motor, app, hold, rel, sps, stepNum = 99):
        if (stepNum == 99):
            self.steps.append((step, motor, app, hold, rel, sps))
        else:
            self.steps.insert(stepNum, (step, motor, app, hold, rel, sps))
        return
    
    #called from the UI to remove a step to the sequence
    def removeStep(self, stepNum=99):
        if (stepNum == 99):
            self.steps.pop(len(self.steps))
        else:
            self.steps.pop(stepNum)
        return

    #called from the UI to change the number of repeats for a sequence
    def changeRepeats(self, rep):
        self.repeats = rep
        return
    
    #runs the steps in the sequence
    def runSequence(self):
        for _ in range(self.repeats):
            for step in self.steps:
                if(step[0] == 0):
                    stepperApply(step[1], step[2], step[5])
                elif(step[0] == 1):
                    stepperRemove(step[1], step[2], step[5])
                elif(step[0] == 2):
                    stepperApplyHoldRelease(step[1], step[2], step[3], step[4], step[5])
        return

#jogs the stepper motor to a specific step value
def jogStepper(motor, steps):
    stepDict[motor].release()
    time.sleep(1) #waits for the chamber to return to zero, might need to be adjusted 

    #after the chanber resets to zero moves the requested number of steps
    for _ in range(steps):
        stepDict[motor].onestep(direction=stepper.FORWARD, )
        time.sleep(0.01)
    return

#a simple fucntion to apply a specific number of steps to a chamber at the rate of sps
def stepperApply(motor, steps, sps):
    for _ in range(steps):
        stepDict[motor].onestep(direction=stepper.FORWARD)
        time.sleep(1/sps)
    return

#a simple fucntion to remove a specific number of steps to a chamber at the rate of sps
def stepperRemove(motor, steps, sps):
    for _ in range(steps):
        stepDict[motor].onestep(direction=stepper.BACKWARD)
        time.sleep(1/sps)
    return

def stepperApplyHoldRelease(motor, app, hold, rel, sps):
    for _ in range(app):
        stepDict[motor].onestep(direction=stepper.FORWARD)
        time.sleep(1/sps)
    time.sleep(hold)
    for _ in range(rel):
        stepDict[motor].onestep(direction=stepper.BACKWARD)
        time.sleep(1/sps)
    return