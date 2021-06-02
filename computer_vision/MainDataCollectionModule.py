import WebcamModule as wM
import DataCollectionModule as dcM
import KeyboardControlModule as kcM
import MotorModule as mM
import cv2 as cv
from time import sleep


maxThrottle = 0.25

##################################
motor = mM.Motor(5, 22, 23, 6, 24, 25)
##################################

MAX_SPEED = 0.8
MIN_SPEED = 0.7
RIGHT_TURN = -1
LEFT_TURN = 1

DELAY = 0.1

recording = False


def record(turn):
    if recording:
        img = wM.get_image(True, size=[240, 120])
        dcM.save_data(img, turn)
    elif not recording:
        dcM.save_log()


while True:

    ####### CONTROL USING KEYBOARD
    kcM.init()

    if kcM.get_keyboard_input('R') or kcM.get_keyboard_input('r'):
        if not recording:
            print('Recording Started ...')
            recording = True
            sleep(0.300)
        else:
            print('Recording Finished ...')
            recording = False
            sleep(0.300)

    if kcM.get_keyboard_input('LEFT'):
        motor.move(MIN_SPEED, LEFT_TURN, DELAY)
        record(LEFT_TURN)
    elif kcM.get_keyboard_input('RIGHT'):
        motor.move(MIN_SPEED, RIGHT_TURN, DELAY)
        record(RIGHT_TURN)
    elif kcM.get_keyboard_input('UP'):
        motor.move(MAX_SPEED, 0, DELAY)
        record()
    elif kcM.get_keyboard_input('DOWN'):
        motor.move(-MAX_SPEED, 0, DELAY)
        record()
    else:
        motor.stop(0.1)

    if cv.waitKey(1) & 0xFF == ord('q'):
        GPIO.cleanup()
        break

    cv.destroyAllWindows()
