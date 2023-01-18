import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import random
from simple_pid import PID

#class to hold the sequence for the mechanical loading
class stepperSequence:
    def __init__(self, rep) -> None:
        self.repeats = rep  #the number of times to repeat a given sequence
        self.steps = []     #an array to hold the sequence

    #called from the UI to add a step to the sequence
    def addStep(self, step, motor, app, hold, rel, sps, stepNum = 99):
        if (stepNum == 99):
            self.steps.append((step, motor, app, hold, rel, sps))
        else:
            self.steps.insert(stepNum, (step, motor, app, hold, rel, sps))
    
    #called from the UI to remove a step to the sequence
    def removeStep(self, stepNum=99):
        if (stepNum == 99):
            self.steps.pop(len(self.steps))
        else:
            self.steps.pop(stepNum)

    #called from the UI to change the number of repeats for a sequence
    def changeRepeats(self, rep):
        self.repeats = rep
    
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

homeSpeed = 0.1 #motor speed to be used when homing the device
mSpeed = .5 #general motor speed before the algo adjusts it


#declares the motor kits at thier given adresses, This order should match the phyical order with hat 4 being closest to the pi and hat 1 being the top of the stack
hat1 = MotorKit()
hat2 = MotorKit(address=0x61)
hat3 = MotorKit(address=0x62)
hat4 = MotorKit(address=0x63)

#holds the values of the stepper so only the number needs passed to the function
stepDict = {
    1: hat2.stepper1,
    2: hat2.stepper2,
    3: hat3.stepper1,
    4: hat3.stepper2,
    5: hat4.stepper1,
    6: hat4.stepper2,
    7: hat1.stepper2
    }
    
#rotates the platform forward
def rForward():
    hat1.motor1.throttle = homeSpeed
    time.sleep(0.1)
    hat1.motor1.throttle = 0

#rotates the platform backward
def rBackward():
    hat1.motor1.throttle = -homeSpeed
    time.sleep(0.1)
    hat1.motor1.throttle = 0   

#rotates the platform left
def rLeft():
    hat1.motor2.throttle = homeSpeed
    time.sleep(0.1)
    hat1.motor2.throttle = 0

#rotates the platform right
def rRight():
    hat1.motor2.throttle = -homeSpeed
    time.sleep(0.1)
    hat1.motor2.throttle = 0

#jogs the stepper motor to a specific step value
def jogStepper(motor, steps):
    stepDict[motor].release()
    time.sleep(1) #waits for the chamber to return to zero, might need to be adjusted 

    #after the chanber resets to zero moves the requested number of steps
    for _ in range(steps):
        stepDict[motor].onestep(direction=stepper.FORWARD)
        time.sleep(0.01)

#a simple fucntion to apply a specific number of steps to a chamber at the rate of sps
def stepperApply(motor, steps, sps):
    for _ in range(steps):
        stepDict[motor].onestep(direction=stepper.FORWARD)
        time.sleep(1/sps)

#a simple fucntion to remove a specific number of steps to a chamber at the rate of sps
def stepperRemove(motor, steps, sps):
    for _ in range(steps):
        stepDict[motor].onestep(direction=stepper.BACKWARD)
        time.sleep(1/sps)

def stepperApplyHoldRelease(motor, app, hold, rel, sps):
    for _ in range(app):
        stepDict[motor].onestep(direction=stepper.FORWARD)
        time.sleep(1/sps)
    time.sleep(hold)
    for _ in range(rel):
        stepDict[motor].onestep(direction=stepper.BACKWARD)
        time.sleep(1/sps)

def gravityRun(target, runTime):
    startTime = time.CLOCK_REALTIME() # finds the start time
    
    pid = PID(1,1,1, setpoint=target, sample_time=30)

    m1adj = 1   #allows for the motor 1 speed to be adjusted from base
    m1dir = 1
    m2adj = 1   #allows for the motor 2 speed to be adjusted from base
    m2dir = 1

    #main loop of the gravity system checks the 
    while (time.CLOCK_REALTIME() - startTime) < runTime:
        hat1.motor1.throttle(mSpeed*m1adj*m1dir)
        hat1.motor2.throttle(mSpeed*m2adj*m2dir)
 
        if(random.choice(range(0,4)) == 1): #1/3 chance motor 1 changes direction
            m1dir*= -1
        if(random.choice(range(0,4)) == 1): #1/3 chance motor 2 changes direction
            m2dir*= -1    

        m2adj = pid(1)
        
        time.sleep(random.choice(range(3,30))) #sleeps from 3 to 60 seconds before setting and checking again

