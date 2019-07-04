import numpy as np
from defines import output, countdown, SCREEN, THRESHOLD, turn_direction,\
                    average_slope_intercept, display_lanes, ROI, get_coordinates
from actions import PressKey, ReleaseKey, W, A, S, D, P
import time
import cv2
import mss.tools

FILE_NAME = "training_data.npy"
training_data = []

# countdown(5)
while True:
    start = time.time()

    #Capturing game screen
    with mss.mss() as sct:
        start = time.time()
        monitor = {"top": 32, "left": 1119, "width": 800, "height": 600}
        sct_img = sct.grab(monitor)
        screen = np.array(sct_img)
        cv2.cvtColor(screen, cv2.COLOR_RGBA2RGB)

        roi = ROI(screen)


        try:
            lines = cv2.HoughLinesP(roi, 1, np.pi/180, 100, np.array([]), minLineLength=300, maxLineGap=200)
            left_lane_paras, right_lane_paras = average_slope_intercept(screen, lines)
            left_lane_coords = get_coordinates(screen, left_lane_paras)
            right_lane_coords = get_coordinates(screen, right_lane_paras)

            display_lanes(screen, left_lane_coords)
            display_lanes(screen, right_lane_coords)
        except:
            pass

        # training_screen = cv2.resize(screen, (80, 60))
        # training_data.append([training_screen, output()])



    cv2.imshow("roi", roi)
    cv2.imshow("screen", screen)
    last_time = time.time()
    # print(len(training_data))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()