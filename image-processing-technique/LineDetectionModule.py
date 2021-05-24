import cv2 as cv
import numpy as np
import utils

curve_list = []
AVERAGE_VALUE = 10


def get_line_curve(image, display=2):
    """
    Given the input frame calculate the lane curve
    :param img:
    :return:
    """

    # Step 1 - Thresholding
    image_thresh = utils.thresholding(image)

    # Step 2 - Warping
    h, w, c = image.shape
    points = utils.get_trackbars_values()
    image_warp = utils.warp_image(image_thresh, points, w, h)
    image_warp_points = utils.draw_points(image.copy(), points)

    # Step 3 -
    middle_point, image_hist = utils.get_histogram(image_warp, min_percentage=0.5, region=4)
    curve_average_point, image_hist = utils.get_histogram(image_warp, min_percentage=0.9, region=1)

    curve_raw = curve_average_point - middle_point

    # Step 4 - Averaging
    curve_list.append(curve_raw)
    if len(curve_list) > AVERAGE_VALUE:
        curve_list.pop(0)

    curve = int(sum(curve_list)/len(curve_list))

    # Step 5 - Display
    if display != 0:
        image_inverse_wrap = utils.warp_image(image_warp, points, w, h, inverse=True)
        image_inverse_wrap = cv.cvtColor(image_inverse_wrap, cv.COLOR_GRAY2BGR)
        image_inverse_wrap[0:h//3, 0:w] = 0, 0, 0

        image_lane_color = np.zeros_like(image)
        image_lane_color[:] = 0, 255, 0
        image_lane_color = cv.bitwise_and(image_inverse_wrap, image_lane_color)
        image_result = cv.addWeighted(image.copy(), 1, image_lane_color, 1, 0)

        midY = 450
        cv.putText(image_result, str(curve), (w//2 - 80, 85), cv.FONT_HERSHEY_COMPLEX, 2, (255,0,0))
        cv.line(image_result, (w//2, midY), (w//2 + (curve*3), midY), (255,0,255), 5)
        cv.line(image_result, ((w//2 + (curve*3)), midY -25), (w//2 + (curve*3), midY), (255,0,255), 5)

        for x in range(-30, 30):
            w = w//2
            cv.line(image_result, (w*x + int(curve//50), midY - 10),
                    (w*x + int(curve//50), midY+10), (0,0,255),2)
    if display == 2:
        image_stacked = utils.stack_images(0.7, (
            # [image, image_lane_color, image_warp],
            [image_hist, image_warp_points, image_result]
        ))
        cv.imshow("Trackbars", image_stacked)
    if display == 1:
        cv.imshow('Result', image_result)

    # Normalization
    curve = curve / 100
    if curve > 1: curve = 1
    if curve < -1: curve = -1

    return curve


if __name__ == '__main__':
    frame_counter = 0
    cap = cv.VideoCapture(0)
    initial_trackbar_values = [87, 74, 0, 240]
    utils.initialize_trackbars(initial_trackbar_values)

    while True:
        frame_counter += 1
        if cap.get(cv.CAP_PROP_FRAME_COUNT) == frame_counter:
            cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            frame_counter = 0

        success, frame = cap.read()
        frame = cv.resize(frame, (480, 680))
        # Temp debug
        frame = cv.transpose(frame)

        curve = get_line_curve(frame, display=2)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv.destroyAllWindows()