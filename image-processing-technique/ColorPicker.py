import cv2 as cv
import numpy as np

frameWidth = 440
frameHeight = 280

cap = cv.VideoCapture('vid1.mp4')
cap.set(3, frameWidth)
cap.set(4, frameHeight)


def empty(a):
    pass


cv.namedWindow("HSV")
cv.resizeWindow("HSV", 840, 640)
cv.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

frame_counter = 0

while True:
    frame_counter += 1
    if cap.get(cv.CAP_PROP_FRAME_COUNT) == frame_counter:
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        frame_counter = 0

    _, img = cap.read()

    img = cv.resize(img, (frameWidth, frameHeight), fx=0, fy=0, interpolation=cv.INTER_CUBIC)

    imgHsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    h_min = cv.getTrackbarPos("HUE Min", "HSV")
    h_max = cv.getTrackbarPos("HUE Max", "HSV")
    s_min = cv.getTrackbarPos("SAT Min", "HSV")
    s_max = cv.getTrackbarPos("SAT Max", "HSV")
    v_min = cv.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv.getTrackbarPos("VALUE Max", "HSV")
    print(h_min)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv.inRange(imgHsv, lower, upper)

    result = cv.bitwise_and(img, img, mask=mask)
    result = cv.resize(result, (frameWidth, frameHeight), fx=0, fy=0, interpolation=cv.INTER_CUBIC)

    mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
    mask = cv.resize(mask, (frameWidth, frameHeight), fx=0, fy=0, interpolation=cv.INTER_CUBIC)

    hStack = np.hstack([img, mask, result])
    cv.imshow('Horizontal Stacking', hStack)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()