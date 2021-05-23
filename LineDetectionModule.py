import cv2 as cv
import numpy as np
import utils


def get_lane_curve(image):
    """
    Given the input frame calculate the lane curve
    :param img:
    :return:
    """

    # Step 1
    image_thresh = utils.thresholding(image)

    # Step 2
    h, w, c = image.shape
    points = utils.get_trackbars_values()
    image_warp = utils.warp_image(image, points, w, h) # image_thresh
    image_warp_points = utils.draw_points(image.copy(), points)

    cv.imshow('Threshold', image_thresh)
    cv.imshow('Warp', image_warp)
    cv.imshow('Image Warp Points', image_warp_points)

    return image_warp


if __name__ == '__main__':
    frame_counter = 0
    cap = cv.VideoCapture("vid1.mp4")
    initial_trackbar_values = [100, 100, 100, 100]
    utils.initialize_trackbars(initial_trackbar_values)

    while True:
        frame_counter += 1
        if cap.get(cv.CAP_PROP_FRAME_COUNT) == frame_counter:
            cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            frame_counter = 0

        success, frame = cap.read()
        frame = cv.resize(frame, (480, 420))
        # frame = cv.resize(frame, (640, 480))

        get_lane_curve(frame)
        cv.imshow('Video', frame)

        cv.waitKey(1)
