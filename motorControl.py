import time
import datetime
from adafruit_motor import stepper
import random
from simple_pid import PID
from adafruit_motorkit import MotorKit
from FaBo9Axis_MPU9250 import MPU9250
import threading
from math import sqrt
import traceback

#declares the motor kits at thier given adresses, This order should match the phyical order with hat 4 being closest to the pi and hat 1 being the top of the stack
hat1 = MotorKit(steppers_microsteps=128)
#hat2 = MotorKit(address=0x61)
#hat3 = MotorKit(address=0x62)
#hat4 = MotorKit(address=0x63)

#Contains all the information for the gravity system
class gravitySystem:

    def __init__(self):
        self.shutdown = False
        self.target = 0
        self.runTime = 30.0
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
        accelRom = MPU9250(address=0x68)

        m1Speed = 1#(self.maxSpeed+self.minSpeed)/2
        m2Speed = .9#(self.maxSpeed+self.minSpeed)/2
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
        motorError = 0
        accelError = 0
        totLoop = 0
        logFile = open('logs/{date:%Y-%m-%d_%H:%M:%S}.csv'.format( date=datetime.datetime.now() ), 'w')
        logFile.write("Loop#, Current X, Current Y, Current Z, Average X, Average Y, Average Z, Gravity\n")

        #main loop of the gravity system checks the 
        while (float(time.time() - startTime) < self.runTime )and self.shutdown == False:
            #sets the speeds of the motors for this loop]
            if(hat1.motor1.throttle != m1Speed*m1dir):
                try:
                    hat1.motor1.throttle = m1Speed*m1dir
                except:
                    print("M1 Call")
                    traceback.print_exc()
                    motorError += 1
                    pass
            if(hat1.motor2.throttle != m2Speed*m2dir):
                try:
                    hat1.motor2.throttle = m2Speed*m2dir
                except:
                    print("M2 Call")
                    traceback.print_exc()
                    motorError += 1
                    pass

            #gets the accelerometer values adds them to the total then calculates the rolling average.
            try:
                accel = accelRom.readAccel()
                xTot += accel['x']
                yTot += accel['y']
                zTot += accel['z']
                
                self.xAvg = xTot/loop
                self.yAvg = yTot/loop
                self.zAvg = zTot/loop
                self.gAvg = sqrt((self.xAvg**2)+(self.yAvg**2)+(self.zAvg**2))
                #s = '{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}}\n'.format(loop, , accel['y'], accel['z'], self.xAvg, self.yAvg, self.zAvg, self.gAvg)
                logFile.write(f"{loop}, {accel['x']}, {accel['y']}, {accel['z']}, {self.xAvg}, {self.yAvg}, {self.zAvg}, {self.gAvg}\n")

                loop += 1

            except:
                
                logFile.write("Unable to get data from accelerometer.\n")
               # traceback.print_exc()
                accelError += 1
                pass
            

            #print("Gravity: ", self.gAvg)

            if(self.target != 0):
                m2Speed = pid(abs(self.gAvg))
                print("Adjusted Speed: ", m2Speed)

            if(loopDirChange > 30): #will attempt to change the direction every 3-30 seconds
                if(random.choice(range(0,9)) == 1): #1/5 chance motor 1 changes direction
                    m1dir = m1dir * -1
                if(random.choice(range(0,9)) == 1): #1/5 chance motor 2 changes direction
                    m2dir = m2dir * -1    
                loopDirChange = 0

            loopDirChange += 1
            totLoop += 1
            time.sleep(0.1)  #loops every tenth of a second
        hat1.motor1.throttle = 0
        hat1.motor2.throttle = 0
        logFile.write(f"Total Loops: {totLoop}\n")
        logFile.write(f"Motor Errors: {motorError}\n")
        logFile.write(f"Accelerometer Errors: {accelError}\n")
        logFile.write(f"Final Gravity: {self.gAvg}\n")
        logFile.close()
        return
