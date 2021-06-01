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

SPEED = 0.5
RIGHT_TURN = -1
LEFT_TURN = 1

DELAY = 0.1

MAX_CURVE_VALUE = 0.3
SENSITIVITY = 0.01



def main(mode='KEYBOARD_CONTROL'):

    ################################################################################
    ############################ CONTROL USING KEYBOARD ############################
    if mode == modes[0]:
        key_control.init()
        if key_control.get_keyboard_input('LEFT'):
            motor.move(SPEED, LEFT_TURN, DELAY)
        elif key_control.get_keyboard_input('RIGHT'):
            motor.move(SPEED, RIGHT_TURN, DELAY)
        elif key_control.get_keyboard_input('UP'):
            motor.move(SPEED, 0, DELAY)
        elif key_control.get_keyboard_input('DOWN'):
            motor.move(-SPEED, 0, DELAY)
        else:
            motor.stop(0.1)


    ################################################################################
    ##################### CONTROL USING LINE FOLLOWING SENSORS #####################
    elif mode == modes[1]:
        sensor1 = LineSensor(18) # terma aristera
        sensor2 = LineSensor(17) # aristera
        sensor3 = LineSensor(20)   # kentriko
        sensor4 = LineSensor(27) # deksia
        sensor5 = LineSensor(21)   # terma deksia

        sensors = [0, 0, 0, 0, 0]
        error = 0

        sensors[0] = int(sensor1.value)
        sensors[1] = int(sensor2.value)
        sensors[2] = int(sensor3.value)
        sensors[3] = int(sensor4.value)
        sensors[4] = int(sensor5.value)

        print(f"sensor1: {sensors[0]}\n")
        print(f"sensor2: {sensors[1]}\n")
        print(f"sensor3: {sensors[2]}\n")
        print(f"sensor4: {sensors[3]}\n")
        print(f"sensor5: {sensors[4]}\n") 

        if((sensors[0]== 0 ) and (sensors[1]== 0 ) and (sensors[2]== 0 ) and (sensors[3]== 0 ) and (sensors[4]== 1 )): error = 4
        elif((sensors[0]== 0 ) and (sensors[1]== 0 ) and (sensors[2]== 0 ) and (sensors[3]== 1 ) and (sensors[4]== 1 )): error = 3
        elif((sensors[0]== 0 ) and (sensors[1]== 0 ) and (sensors[2]== 0 ) and (sensors[3]== 1 ) and (sensors[4]== 0 )): error = 2
        elif((sensors[0]== 0 ) and (sensors[1]== 0 ) and (sensors[2]== 1 ) and (sensors[3]== 1 ) and (sensors[4]== 0 )): error = 1
        elif((sensors[0]== 0 ) and (sensors[1]== 0 ) and (sensors[2]== 1 ) and (sensors[3]== 0 ) and (sensors[4]== 0 )): error = 0
        elif((sensors[0]== 0 ) and (sensors[1]== 1 ) and (sensors[2]== 1 ) and (sensors[3]== 0 ) and (sensors[4]== 0 )): error = -1
        elif((sensors[0]== 0 ) and (sensors[1]== 1 ) and (sensors[2]== 0 ) and (sensors[3]== 0 ) and (sensors[4]== 0 )): error = -2
        elif((sensors[0]== 1 ) and (sensors[1]== 1 ) and (sensors[2]== 0 ) and (sensors[3]== 0 ) and (sensors[4]== 0 )): error = -3
        elif((sensors[0]== 1 ) and (sensors[1]== 0 ) and (sensors[2]== 0 ) and (sensors[3]== 0 ) and (sensors[4]== 0 )): error = -4

        print(f"Error: {error}\n\n")

        # ## Go Forward
        # if left_detect == 0 and right_detect == 0:
        #     motor.move(SPEED, 0, DELAY)
        # ## Turn Left
        # elif left_detect == 0 and right_detect == 1:
        #     motor.move(SPEED, LEFT_TURN, DELAY)
        # ## Turn Right
        # elif left_detect == 1 and right_detect == 0:
        #     motor.move(SPEED, RIGHT_TURN, DELAY)

        # ## Stop
        # if left_detect == 1 and right_detect == 1:
        #     motor.stop()


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
            motor.move(SPEED, -steering)
        else:
            motor.move(SPEED, -steering)

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

