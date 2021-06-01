import cv2 as cv
import numpy as np
from image_processing.ColorPicker import ColorPicker


def thresholding(frame):
    """
    Apply thresholding to the input frame by masking out the line
    :param frame:frame
    :return :thresholded_frame
    """

    # Pick color limits
#     color_picker = ColorPicker()
#     img, mask, result = color_picker.pick_color(frame)
#     hStack = np.hstack([img, mask, result])
#     cv.imshow('Color Picker', hStack)

    # Convert frame to HSV space
    img_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Create a range using values selected experimental from ColorPicker
    lower_color = np.array([0, 0, 0])
    upper_color = np.array([179, 255, 79])
    #lower_color, upper_color = color_picker.get_picked_colors()

    # Apply range
    thresholded_frame = cv.inRange(img_hsv, lower_color, upper_color)

    return thresholded_frame


def warp_image(image, input_points, w, h, inverse=False):
    input_points = np.float32(input_points)
    target_points = np.float32([[0, 0], [w, 0], [0, h], [w, h]])

    if inverse:
        transformation_matrix = cv.getPerspectiveTransform(target_points, input_points)
    else:
        transformation_matrix = cv.getPerspectiveTransform(input_points, target_points)

    image_warp = cv.warpPerspective(image, transformation_matrix, (w, h))

    return image_warp


def initialize_trackbars(initial_trackbar_vals, w=480, h=240):
    cv.namedWindow("Trackbars")
    cv.resizeWindow("Trackbars", 360, 240)
    cv.createTrackbar("Width Top", "Trackbars", initial_trackbar_vals[0], w // 2, nothing)
    cv.createTrackbar("Height Top", "Trackbars", initial_trackbar_vals[1], h, nothing)
    cv.createTrackbar("Width Bottom", "Trackbars", initial_trackbar_vals[2], w // 2, nothing)
    cv.createTrackbar("Height Bottom", "Trackbars", initial_trackbar_vals[3], h, nothing)


def get_trackbars_values(w=480, h=240):
    width_top = cv.getTrackbarPos("Width Top", "Trackbars")
    height_top = cv.getTrackbarPos("Height Top", "Trackbars")
    width_bottom = cv.getTrackbarPos("Width Bottom", "Trackbars")
    height_bottom = cv.getTrackbarPos("Height Bottom", "Trackbars")

    points = np.float32([(width_top, height_top), (w - width_top, height_top),
                         (width_bottom, height_bottom), (w - width_bottom, height_bottom)])
    return points


def draw_points(image, points):
    for x in range(4):
        cv.circle(image, (int(points[x][0]), int(points[x][1])), 15, (0, 0, 255), cv.FILLED)

    return image


def nothing(a):
    pass


def get_histogram(image, min_percentage=0.1, region=1, display=True):
    if region == 1:
        # Sum all pixels in y axis
        hist_values = np.sum(image, axis=0)
    else:
        # Sum all pixels in y axis
        hist_values = np.sum(image[image.shape[0] // region:, :], axis=0)

    # Find the min and max values
    max_value = np.max(hist_values)
    min_value = min_percentage * max_value

    # filter the histogram values,omitting the law values
    indexed_array = np.where(hist_values >= min_value)
    # Find the base point using the average value
    base_point = int(np.average(indexed_array))

    if display:
        image_hist = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
        for x, intensity in enumerate(hist_values):
            cv.line(image_hist, (x, image.shape[0]), (x, image.shape[0] - int(intensity) // 255 // region),
                    (255, 0, 255), 1)
            cv.circle(image_hist, (base_point, image.shape[0]), 30, (0, 255, 255), cv.FILLED)
        return base_point, image_hist

    return base_point


def stack_images(scale, image_array):
    rows = len(image_array)
    cols = len(image_array[0])
    rows_available = isinstance(image_array[0], list)
    width = image_array[0][0].shape[1]
    height = image_array[0][0].shape[0]

    if rows_available:
        for x in range(0, rows):
            for y in range(0, cols):
                if image_array[x][y].shape[:2] == image_array[0][0].shape[:2]:
                    image_array[x][y] = cv.resize(image_array[x][y], (0, 0), None, scale, scale)
                else:
                    image_array[x][y] = cv.resize(image_array[x][y],
                                                  (image_array[0][0].shape[1], image_array[0][0].shape[0]),
                                                  image_array[x][y], scale, scale)
                if len(image_array[x][y].shape) == 2:
                    image_array[x][y] = cv.cvtColor(image_array[x][y], cv.COLOR_GRAY2BGR)

        image_blank = np.zeros((height, width, 3), np.uint8)
        hor = [image_blank] * rows
        for x in range(0, rows):
            hor[x] = np.stack(image_array[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if image_array[x].shape[:2] == image_array[0].shape[:2]:
                image_array[x] = cv.resize(image_array[x], (0, 0), None, scale, scale)
            else:
                image_array[x] = cv.resize(image_array[x],
                                           (image_array[0].shape[1], image_array[0].shape[0]),
                                           image_array[x], scale, scale)
            if len(image_array[x].shape) == 2:
                image_array[x] = cv.cvtColor(image_array[x], cv.COLOR_GRAY2BGR)
        hor = np.hstack(image_array)
        ver = hor
    return ver
