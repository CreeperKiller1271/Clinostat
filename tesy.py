from FaBo9Axis_MPU9250 import MPU9250
import time
import sys
from adafruit_motorkit import MotorKit

hat1 = MotorKit()
mpu9250 = MPU9250(address=0x68)

hat1.motor1.throttle = 1
hat1.motor2.throttle = 1
time.sleep(10)
hat1.motor1.throttle = 0
hat1.motor2.throttle = 0

while True:
    accel = mpu9250.readAccel()
    print ("Accel ax = " , accel['x'], " ay = " , accel['y'], " az = " , accel['z'])

    time.sleep(.1)
