import time
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

hat1 = MotorKit(steppers_microsteps=128)
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

#0while(1):
for _ in range(50):
    stepDict[8].onestep()#style=stepper.MICROSTEP, direction=stepper.FORWARD)
    time.sleep(.02)
    #for _ in range(14000):
    #    stepDict[8].onestep(style=stepper.MICROSTEP, direction=stepper.BACKWARD)
    #    time.sleep(1/7000)

stepDict[8].release()