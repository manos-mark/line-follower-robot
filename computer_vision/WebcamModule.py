"""
-This module gets an image through the webcam
using the opencv package
-Display can be turned on or off
-Image size can be defined
"""

import cv2 as cv

cap = cv.VideoCapture(0)


def get_image(display=False, size=[480, 240]):
    _, img = cap.read()
    img = cv.resize(img, (size[0], size[1]))

    if display:
        cv.imshow("Image", img)
    return img


if __name__ == '__main__':
    while True:
        img = get_image(True)
