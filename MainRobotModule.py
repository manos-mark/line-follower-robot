from MotorModule import Motor
from LineDetectionModule import get_line_curve
from WebcamModule import get_image
import cv2 as cv
# import RPi.GPIO as GPIO
import KeyboardControlModule as key_control
from gpiozero import LineSensor


##################################
motor = Motor(5, 22, 23, 6, 24, 25)
##################################

MAX_SPEED = 0.8
MIN_SPEED = 0.6
RIGHT_TURN = -1
LEFT_TURN = 1
MAX_CURVE_VALUE = 0.3
SENSITIVITY = 0.01
modes = ('KEYBOARD_CONTROL', 'LINE_FOLLOWING', 'CUSTOM_IMAGE_PROCESSING', 'DEEP_IMAGE_PROCESSING')


def main(mode='KEYBOARD_CONTROL'):


    ####### CONTROL USING KEYBOARD
    if mode == modes[0]:
        key_control.init()
        if key_control.get_keyboard_input('LEFT'):
            motor.move(MAX_SPEED, LEFT_TURN, 0.1)
        elif key_control.get_keyboard_input('RIGHT'):
            motor.move(MIN_SPEED, RIGHT_TURN, 0.1)
        elif key_control.get_keyboard_input('UP'):
            motor.move(MIN_SPEED, 0, 0.1)
        elif key_control.get_keyboard_input('DOWN'):
            motor.move(-MAX_SPEED, 0, 0.1)
        else:
            motor.stop(0.1)

    ####### CONTROL USING LINE FOLLOWING SENSORS
    if mode == modes[1]:
        left_sensor = LineSensor(17)
        right_sensor = LineSensor(27)
        left_detect = int(left_sensor.value)
        right_detect = int(right_sensor.value)

        ## Go Forward
        if left_detect == 0 and right_detect == 0:
            motor.move(MAX_SPEED, 0, 0.1)
        ## Turn Left
        elif left_detect == 0 and right_detect == 1:
            motor.move(MIN_SPEED, LEFT_TURN, 0.1)
        ## Turn Right
        elif left_detect == 1 and right_detect == 0:
            motor.move(MIN_SPEED, RIGHT_TURN, 0.1)

        ## Stop
        if left_detect == 1 and right_detect == 1:
            motor.stop()


    ####### CONTROL USING CUSTOM IMAGE PROCESSING
    # elif mode == modes[2]:
    #     img = get_image()
    #
    #     curve_value = get_line_curve(img, 2)
    #     print(f"curve_value : {curve_value}")
    #     if curve_value > MAX_CURVE_VALUE:
    #         curve_value = MAX_CURVE_VALUE
    #     if curve_value < -MAX_CURVE_VALUE:
    #         curve_value = -MAX_CURVE_VALUE
    #
    #     if curve_value > 0:
    #         # SENSITIVITY = 1.7
    #         if curve_value < 0.05:
    #             curve_value = 0
    #     else:
    #         if curve_value > -0.08:
    #             curve_value = 0
    #
    #     motor.move(SPEED, -curve_value*SENSITIVITY, 0.05)

    ####### CONTROL USING DEEP IMAGE PROCESSING
    # elif mode == modes[3]:


if __name__ == '__main__':

    while True:
        main()

        if cv.waitKey(1) & 0xFF == ord('q'):
            GPIO.cleanup()
            break

    cv.destroyAllWindows()

