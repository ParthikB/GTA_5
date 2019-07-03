import cv2
from PIL import ImageGrab
import numpy as np
import time
import mss.tools
from ExtractKeys import input_key


SCREEN = [1119, 32, 1919, 632]
THRESHOLD =250

def output():
    output = [0,0,0]
    if input_key() == ["A"]:
        output = [1,0,0]
    elif input_key() == ["W"]:
        output = [0,1,0]
    elif input_key() == ["D"]:
        output = [0,0,1]
    return output


def processed_img(screen):
    # gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(screen, threshold1=200, threshold2=200)
    processed_img = cv2.GaussianBlur(processed_img, ksize=(7,7), sigmaX=1)
    mask = np.zeros(processed_img.shape, dtype=np.uint8)
    roi_corners = np.array([[(0, 400), (300, 280), (500, 280), (800, 400), (800, 600), (700, 600), (400, 280),
                             (180, 600), (0, 600)]], dtype=np.int32)
    cv2.fillPoly(mask, roi_corners, 255)

    roi = cv2.bitwise_and(processed_img, mask)

    try:
        lines = cv2.HoughLinesP(roi, 1, np.pi/180, THRESHOLD, np.array([]),minLineLength=300, maxLineGap=150)
        slope_log = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(screen, (x1, y1), (x2, y2), (0, 255, 0), 8)
            slope_log.append(slope(x1, x2, y1, y2))
    except:
        pass

    return roi, slope_log

def countdown(x):
    for i in list(range(x-1))[::-1]:
        print(i+1)
        time.sleep(1)

def slope(x1, x2, y1, y2):
    try:
        slope = round(((y2-y1)/(x2-x1)),2)
    except:
        pass
    return slope


def turn(slope_log):
    p_slope = []
    n_slope = []
    for m in slope_log:
        if m > 0:
            p_slope.append(m)
        else:
            n_slope.append(m)

    if len(p_slope) > 0 and len(n_slope) > 0:
        move = 'forward'
    elif len(p_slope) == 0 and len(n_slope) > 0:
        move = 'right'
    elif len(p_slope) > 0 and len(n_slope) == 0:
        move = 'left'
    try:
        if len(p_slope) == 0 and len(n_slope) == 0:
            move = 'none'
    except:
        pass

    return move

