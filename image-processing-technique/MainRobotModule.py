from MotorModule import Motor
from LineDetectionModule import get_line_curve
from WebcamModule import get_image
import cv2 as cv
import RPi.GPIO as GPIO
import KeyboardControlModule as key_control


##################################
motor = Motor(5, 22, 23, 6, 24, 25)
##################################

SPEED = 0.60
MAX_CURVE_VALUE = 0.3
SENSITIVITY = 0.01


def main():
    key_control.init()

    if key_control.get_keyboard_input('LEFT'):
        motor.move(SPEED, 0.3, 0.1)
    elif key_control.get_keyboard_input('RIGHT'):
        motor.move(SPEED, -0.3, 0.1)
    elif key_control.get_keyboard_input('UP'):
        motor.move(SPEED, 0, 0.1)
    elif key_control.get_keyboard_input('DOWN'):
        motor.move(-SPEED, 0, 0.1)
    else:
        motor.stop(0.1)

    # img = get_image()

    # curve_value = get_line_curve(img, 2)
    # print(f"curve_value : {curve_value}")
    # if curve_value > MAX_CURVE_VALUE:
    #     curve_value = MAX_CURVE_VALUE
    # if curve_value < -MAX_CURVE_VALUE:
    #     curve_value = -MAX_CURVE_VALUE

    # if curve_value > 0:
    #     # SENSITIVITY = 1.7
    #     if curve_value < 0.05:
    #         curve_value = 0
    # else:
    #     if curve_value > -0.08:
    #         curve_value = 0

    # motor.move(SPEED, -curve_value*SENSITIVITY, 0.05)


if __name__ == '__main__':
    while True:
        main()
        if cv.waitKey(1) & 0xFF == ord('q'):
            GPIO.cleanup()
            break

    cv.destroyAllWindows()

