"""
This module allows creation of robot objects for 2 or 4 wheeled robots.
The motor driver used is the L298n.
The base package used is the Rpi GPIO
"""

import Rpi.GPIO as GPIO
from time import sleep
GPIO.setmode(GRPIO.BCM)
GPIO.setwarnings(False)


class Motor:
    def __init__(self, enable_right, right_forward, right_backward, enable_left, left_forward, left_backward):
        self.enable_right = enable_right
        self.right_forward = right_forward
        self.right_backward = right_backward
        self.enable_left = enable_left
        self.left_forward = left_forward
        self.left_backward = left_backward

        GPIO.setup(self.enable_right, GPIO.OUT)
        GPIO.setup(self.right_forward, GPIO.OUT)
        GPIO.setup(self.right_backward, GPIO.OUT)
        GPIO.setup(self.enable_left, GPIO.OUT)
        GPIO.setup(self.left_forward, GPIO.OUT)
        GPIO.setup(self.left_backward, GPIO.OUT)

        self.pwmA = GPIO.PWM(self.enable_right, 100)
        self.pwmB = GPIO.PWM(self.enable_left, 100)

        self.pwmA.start(0)
        self.pwmB.start(0)
        self.my_speed = 0

    def move(self, speed=0.5, turn=0, t=0):
        speed *= 100
        turn *= 70
        left_speed = speed - turn
        right_speed = speed - turn

        if left_speed > 100: left_speed = 100
        elif left_speed < -100: left_speed = -100
        if right_speed > 100: right_speed = 100
        elif right_speed < -100: right_speed = -100

        self.pwmA.ChangeDutyCycle(abs(left_speed))
        self.pwmB.ChangeDutyCycle(abs(right_speed))

        if left_speed > 0:
            GPIO.output(self.right_forward, GPIO.HIGH)
            GPIO.output(self.right_backward, GPIO.LOW)
        else:
            GPIO.output(self.right_forward, GPIO.LOW)
            GPIO.output(self.right_backward, GPIO.HIGH)
        if right_speed > 0:
            GPIO.output(self.left_forward, GPIO.HIGH)
            GPIO.output(self.left_backward, GPIO.LOW)
        else:
            GPIO.output(self.left_forward, GPIO.LOW)
            GPIO.output(self.left_backward, GPIO.HIGH)

        sleep(t)

    def stop(self, t=0):
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        self.my_speed = 0
        sleep(t)


def main():
    motor.move(0.5, 0.2)
    motor.stop(2)
    motor.move(-0.5, 0.2)
    motor.stop(2)


if __name__ == '__main__':
    motor = Motor(2,3,4,17,22,27)
    main()