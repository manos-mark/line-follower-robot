import cv2 as cv
import numpy as np


class ColorPicker:
    def __init__(self, width=480, height=280):
        self.width = width
        self.height = height

        self.v_min = self.s_min = self.h_min = 0
        self.h_max = 179
        self.v_max = self.s_max = 255

        self.lower_colors = np.array([self.h_min, self.s_min, self.v_min])
        self.upper_colors = np.array([self.h_max, self.s_max, self.v_max])

        cv.namedWindow("Color Picker")
        cv.resizeWindow("Color Picker", 840, 640)
        cv.createTrackbar("HUE Min", "Color Picker", self.h_min, self.h_max, self.empty)
        cv.createTrackbar("HUE Max", "Color Picker", self.h_max, self.h_max, self.empty)
        cv.createTrackbar("SAT Min", "Color Picker", self.s_min , self.s_max, self.empty)
        cv.createTrackbar("SAT Max", "Color Picker", self.s_max, self.s_max, self.empty)
        cv.createTrackbar("VALUE Min", "Color Picker", self.v_min, self.v_max, self.empty)
        cv.createTrackbar("VALUE Max", "Color Picker", 79, self.v_max, self.empty)

    def pick_color(self, img):
        # Temp debug
        img = cv.transpose(img)

        img = cv.transpose(img)  # Temp debug
        img = cv.resize(img, (self.width, self.height), fx=0, fy=0, interpolation=cv.INTER_CUBIC)
        image_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        self.h_min = cv.getTrackbarPos("HUE Min", "Color Picker")
        self.h_max = cv.getTrackbarPos("HUE Max", "Color Picker")
        self.s_min = cv.getTrackbarPos("SAT Min", "Color Picker")
        self.s_max = cv.getTrackbarPos("SAT Max", "Color Picker")
        self.v_min = cv.getTrackbarPos("VALUE Min", "Color Picker")
        self.v_max = cv.getTrackbarPos("VALUE Max", "Color Picker")

        self.lower_colors = np.array([self.h_min, self.s_min, self.v_min])
        self.upper_colors = np.array([self.h_max, self.s_max, self.v_max])

        mask = cv.inRange(image_hsv, self.lower_colors, self.upper_colors)

        result = cv.bitwise_and(img, img, mask=mask)
        result = cv.resize(result, (self.width, self.height), fx=0, fy=0, interpolation=cv.INTER_CUBIC)

        mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
        mask = cv.resize(mask, (self.width, self.height), fx=0, fy=0, interpolation=cv.INTER_CUBIC)

        return img, mask, result

    def get_picked_colors(self):
        return self.lower_colors, self.upper_colors

    def empty(self, a):
        pass


def main():
    cap = cv.VideoCapture('vid2.mp4')
    cap.set(3, 440)
    cap.set(4, 280)

    frame_counter = 0
    while True:
        frame_counter += 1
        if cap.get(cv.CAP_PROP_FRAME_COUNT) == frame_counter:
            cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            frame_counter = 0

        _, img = cap.read()
        img, mask, result = color_picker.pick_color(img)

        hStack = np.hstack([img, mask, result])
        cv.imshow('Color Picker', hStack)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    color_picker = ColorPicker()
    main()
