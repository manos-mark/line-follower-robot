from MotorModule import Motor
from image_processing.LineDetectionModule import get_line_curve
from WebcamModule import get_image
import cv2 as cv
# import RPi.GPIO as GPIO
import computer_vision.KeyboardControlModule as key_control
from gpiozero import LineSensor


##################################
motor = Motor(5, 22, 23, 6, 24, 25)
##################################

modes = ('KEYBOARD_CONTROL', 'LINE_FOLLOWING', 'CUSTOM_IMAGE_PROCESSING', 'DEEP_IMAGE_PROCESSING')

SPEED = 50
RIGHT_TURN = -1
LEFT_TURN = 1

DELAY = 0.2

MAX_CURVE_VALUE = 0.3
SENSITIVITY = 0.01



def main(mode='KEYBOARD_CONTROL'):

    ################################################################################
    ############################ CONTROL USING KEYBOARD ############################
    if mode == modes[0]:
        key_control.init()
        if key_control.get_keyboard_input('LEFT'):
            motor.turn_left(SPEED, DELAY)
        elif key_control.get_keyboard_input('RIGHT'):
            motor.turn_right(SPEED, DELAY)
        elif key_control.get_keyboard_input('UP'):
            motor.forward(SPEED, DELAY)
        elif key_control.get_keyboard_input('DOWN'):
            motor.backward(SPEED, DELAY)
        else:
            motor.stop(0.1)


    ################################################################################
    ##################### CONTROL USING LINE FOLLOWING SENSORS #####################
    elif mode == modes[1]:
        left_sensor = LineSensor(17)
        right_sensor = LineSensor(27)
        left_detect = int(left_sensor.value)
        right_detect = int(right_sensor.value)

        ## Go Forward
        if left_detect == 0 and right_detect == 0:
            motor.forward(SPEED, DELAY)
        ## Turn Left
        elif left_detect == 0 and right_detect == 1:
            motor.turn_left(SPEED, DELAY)
        ## Turn Right
        elif left_detect == 1 and right_detect == 0:
            motor.turn_right(SPEED, DELAY)

        ## Stop
        if left_detect == 1 and right_detect == 1:
            motor.stop()


    #################################################################################
    ##################### CONTROL USING CUSTOM IMAGE PROCESSING #####################
    elif mode == modes[2]:
        img = get_image()
    
        curve_value = get_line_curve(img, 2)
        print(f"curve_value : {curve_value}")
        if curve_value > MAX_CURVE_VALUE:
            curve_value = MAX_CURVE_VALUE
        if curve_value < -MAX_CURVE_VALUE:
            curve_value = -MAX_CURVE_VALUE
    
        if curve_value > 0:
            # SENSITIVITY = 1.7
            if curve_value < 0.05:
                curve_value = 0
        else:
            if curve_value > -0.08:
                curve_value = 0
    
        motor.move(SPEED, -curve_value*SENSITIVITY, 0.05)


    ###############################################################################
    ##################### CONTROL USING DEEP IMAGE PROCESSING #####################
    elif mode == modes[3]:
        img = get_image(True, size=[240,120])
        img = np.asarray(img)
        img = preprocess(img)
        img = np.array([img])

        steering = float(model.predict(img))
        
        if steering != 0:
            motor.move(MIN_SPEED, -steering)
        else:
            motor.move(MAX_SPEED, -steering)

def preprocess(img):
    img = img[54:120, :, :]
    img = cv.cvtColor(img, cv.COLOR_RGB2YUV)
    img = cv.GaussianBlur(img, (3,3), 0)
    img = cv.resize(img, (200, 66))
    img = img / 255
    return img


if __name__ == '__main__':
#     model = load_model('/home/')
    
    while True:
        main('LINE_FOLLOWING')

        if cv.waitKey(1) & 0xFF == ord('q'):
            GPIO.cleanup()
            break

    cv.destroyAllWindows()

