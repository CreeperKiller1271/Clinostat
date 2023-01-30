import time
from adafruit_motor import stepper
import random
from simple_pid import PID
from adafruit_motorkit import MotorKit
from qwiic_icm20948 import QwiicIcm20948
import threading

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
        self.rThread = threading.Thread(target=self.gravityRun)
        self.shutdown = False
        self.target = 0
        self.runTime = 30
        self.accelRom = QwiicIcm20948(0x66)
        self.minSpeed = .8 #motor speed to be used when homing the device
        self.maxSpeed = 1 #general motor speed before the algo adjusts it

    def run(self):
        self.rThread.start()

    def stop(self):
        self.shutdown = True

    def setup(self, target: int, runTime: int):
        self.target = target
        self.runTime = runTime

    def setSpeed(self, miSpeed: int, maSpeed: int):
        self.minSpeed = miSpeed
        self.maxSpeed = maSpeed

    #rotates the platform forward
    def rForward(self):
        hat1.motor1.throttle = self.minSpeed
        time.sleep(0.1)
        hat1.motor1.throttle = 0
        return

    #rotates the platform backward
    def rBackward(self):
        hat1.motor1.throttle = -self.minSpeed
        time.sleep(0.1)
        hat1.motor1.throttle = 0 
        return  

    #rotates the platform left
    def rLeft(self):
        hat1.motor2.throttle = self.minSpeed
        time.sleep(0.1)
        hat1.motor2.throttle = 0
        return

    #rotates the platform right
    def rRight(self):
        hat1.motor2.throttle = -self.minSpeed
        time.sleep(0.1)
        hat1.motor2.throttle = 0
        return

    def gravityRun(self):
        startTime = time.time() # finds the start time

        self.accelRom.begin()

        pid = PID(1,1,1, setpoint=self.target, sample_time=30)
        pid.output_limits = (self.minSpeed, 1)

        m1adj = 1   #allows for motor 1's speed to be adjusted from base
        m1dir = 1   #allows for motor 1 to flip its direction
        m2adj = 1   #allows for motor 2's speed to be adjusted from base
        m2dir = 1   #allows for motor 2 to flip its direction

        #main loop of the gravity system checks the 
        while (time.time() - startTime) < self.runTime and self.shutdown == False:
            hat1.motor1.throttle = self.maxSpeed*m1adj*m1dir
            hat1.motor2.throttle = self.maxSpeed*m2adj*m2dir
    
            if(random.choice(range(0,4)) == 1): #1/3 chance motor 1 changes direction
                m1dir = m1dir * -1
            if(random.choice(range(0,4)) == 1): #1/3 chance motor 2 changes direction
                m2dir = m2dir * -1    

            if(self.target != 0):
                m2adj = pid(1)
            
            time.sleep(5)#random.choice(range(3,30))) #sleeps from 3 to 60 seconds before setting and checking again
            self.accelRom.getAgmt()
            print(self.accelRom.ayRaw)
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