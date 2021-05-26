from gpiozero import Robot, LineSensor
from time import sleep
import RPi.GPIO as GPIO
robot = Robot(left=(24, 25), right=(22, 23))
left_sensor = LineSensor(17)
right_sensor= LineSensor(27)

def move():
    
    left_motor = 0
    right_motor = 0
    right_motor_speed = 0.65
    left_motor_speed = 0.65
            
    while True:
        left_detect  = int(left_sensor.value)
        right_detect = int(right_sensor.value)
        
        ## Go Forward
        if left_detect == 0 and right_detect == 0:
            left_motor = 1
            right_motor = 1
            right_motor_speed = 0.65
            left_motor_speed = 0.65
            
        ## Turn Left
        if left_detect == 0 and right_detect == 1:
            left_motor = -1
            right_motor = 1
            right_motor_speed = 0.65
            left_motor_speed = 0.45
        
        ## Turn Right
        if left_detect == 1 and right_detect == 0:
            right_motor = -1
            left_motor = 1
            right_motor_speed = 0.45
            left_motor_speed = 0.65
            
        ## Stop
        if left_detect == 1 and right_detect == 1:
            left_motor = 0
            right_motor = 0
            right_motor_speed = 0
            left_motor_speed = 0
            
        #print(r, l)
        yield (right_motor * right_motor_speed, left_motor * left_motor_speed)

robot.source = move()

sleep(6000)
robot.stop()
robot.source = None
robot.close()
left_sensor.close()
right_sensor.close()
GPIO.cleanup()
