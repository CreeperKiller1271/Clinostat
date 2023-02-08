from FaBo9Axis_MPU9250 import MPU9250
import time
import sys

mpu9250 = MPU9250(address=0x68)

while True:
    accel = mpu9250.readAccel()
    print ("Accel ax = " , accel['x'], " ay = " , accel['y'], " az = " , accel['z'])

    time.sleep(.1)
