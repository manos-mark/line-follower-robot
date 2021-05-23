import cv2 as cv
import numpy as np


def thresholding(frame):
    """
    Apply thresholding to the input frame by masking out the line
    :param frame:frame
    :return :thresholded_frame
    """
    # Convert frame to HSV space
    img_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # Create a range using values selected experimental from ColorPicker
    lower_color = np.array([80, 0, 0])
    upper_color = np.array([255, 160, 255])
    # Apply range
    thresholded_frame = cv.inRange(img_hsv, lower_color, upper_color)

    return thresholded_frame


def warp_image(image, input_points, w, h):
    input_points = np.float32(input_points)
    target_points = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    transformation_matrix = cv.getPerspectiveTransform(input_points, target_points)
    image_warp = cv.warpPerspective(image, transformation_matrix, (w, h))

    return image_warp


def initialize_trackbars(initial_trackbar_vals, w=480, h=240):
    cv.namedWindow("Trackbars")
    cv.resizeWindow("Trackbars", 360, 240)
    cv.createTrackbar("Width Top", "Trackbars", initial_trackbar_vals[0], w//2, nothing)
    cv.createTrackbar("Height Top", "Trackbars", initial_trackbar_vals[1], h, nothing)
    cv.createTrackbar("Width Bottom", "Trackbars", initial_trackbar_vals[2], w//2, nothing)
    cv.createTrackbar("Height Bottom", "Trackbars", initial_trackbar_vals[3], h, nothing)


def get_trackbars_values(w=480, h=240):
    width_top = cv.getTrackbarPos("Width Top", "Trackbars")
    height_top = cv.getTrackbarPos("Height Top", "Trackbars")
    width_bottom = cv.getTrackbarPos("Width Bottom", "Trackbars")
    height_bottom = cv.getTrackbarPos("Height Bottom", "Trackbars")

    points = np.float32([(width_top, height_top), (w-width_top, height_top),
                         (width_bottom, height_bottom), (w-width_bottom, height_bottom)])
    return points


def draw_points(image, points):
    for x in range(4):
        cv.circle(image, (int(points[x][0]), int(points[x][1])), 15, (0,0,255), cv.FILLED)

    return image


def nothing():
    pass

