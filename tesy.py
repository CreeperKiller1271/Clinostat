from FaBo9Axis_MPU9250 import MPU9250
import time
import sys

mpu9250 = MPU9250()

while True:
    accel = mpu9250.readAccel()
    print (" ax = %d" , accel['x'])
    print (" ay = %d" , accel['y'])
    print (" az = %d" , accel['z'])

    time.sleep(.5)
