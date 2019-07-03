import numpy as np
from Defines import output, countdown, SCREEN, THRESHOLD, processed_img, turn
from Actions import PressKey, ReleaseKey, W, A, S, D, P
import time
import cv2
import mss.tools

FILE_NAME = "training_data.npy"
training_data = []

countdown(5)
while True:
    start = time.time()

    #Capturing game screen
    with mss.mss() as sct:
        start = time.time()
        monitor = {"top": 32, "left": 1119, "width": 800, "height": 600}
        sct_img = sct.grab(monitor)
        screen = np.array(sct_img) #

    training_screen = cv2.resize(screen, (80, 60))
    training_data.append([training_screen, output()])

    roi, slope_log = processed_img(screen)
    move = turn(slope_log)

    # print(output())
    cv2.imshow("test", training_screen)
    cv2.imshow("screen", screen)
    # cv2.imshow("ROI", roi)
    # print("FPS:", 1 / (time.time() - start))
    last_time = time.time()
    print(len(training_data))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()