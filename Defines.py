import cv2
from PIL import ImageGrab
import numpy as np
import time
import mss.tools
from extractKeys import input_key


SCREEN = [1119, 32, 1919, 632]
THRESHOLD =250

def display_lanes(screen, lane_coords):
    x1, y1, x2, y2 = lane_coords
    cv2.line(screen, (x1, y1), (x2, y2), (0, 255, 0), 8)


def ROI(screen):
    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, threshold1=150, threshold2=200)
    blur = cv2.GaussianBlur(canny, ksize=(3,3), sigmaX=1)

    # roi_vertices = np.array([[(0, 440), (270, 290), (540, 290), (800, 400),
    #                          (800, 600), (500, 600), (400, 310), (330, 600), (0, 600)]], dtype=np.int32)
    roi_vertices = np.array([[(0, 400), (300, 280), (500, 280), (800, 400), (800, 600), (700, 600), (400, 280),
       (180, 600), (0, 600)]], dtype=np.int32)
    mask = np.zeros_like(gray)
    cv2.fillPoly(mask, roi_vertices, 255)
    ROI = cv2.bitwise_and(blur, mask)
    return ROI


def get_coordinates(screen, lane_para):
    slope, intercept = lane_para
    if slope != 0:
        y1 = screen.shape[0]
        y2 = int(y1 * (1/2))
        x1 = int((y1-intercept)/slope)
        x2 = int((y2-intercept)/slope)
        return np.array([x1, y1, x2, y2])
    else:
        return np.array([0, 0, 0, 0])



def average_slope_intercept(screen, lines):
    left_fit = []
    right_fit = []
    parameters_log = []

    for line in lines:
        x1, y1, x2, y2 = line[0]
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        parameters_log.append(parameters)

    parameters_log = np.array(parameters_log).reshape(-1, 2)

    for data in parameters_log:
        if data[0] > 0:
            right_fit.append([data[0], data[1]])
        else:
            left_fit.append([data[0], data[1]])

    right_fit = np.array(right_fit).reshape(-1, 2)
    left_fit = np.array(left_fit).reshape(-1, 2)

    if len(left_fit) != 0:
        left_lane_average = np.average(left_fit, axis=0)
    else:
        left_lane_average = [0, 0]
    if len(right_fit) != 0:
        right_lane_average = np.average(right_fit, axis = 0)
    else:
        right_lane_average = [0, 0]

    return np.array(left_lane_average), np.array(right_lane_average)


def output():
    output = [0,0,0]
    if input_key() == ["A"]:
        output = [1,0,0]
    elif input_key() == ["W"]:
        output = [0,1,0]
    elif input_key() == ["D"]:
        output = [0,0,1]
    return output


# def get_lanes(screen):
#     # gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
#     processed_img = cv2.Canny(screen, threshold1=200, threshold2=200)
#     processed_img = cv2.GaussianBlur(processed_img, ksize=(7,7), sigmaX=1)
#     mask = np.zeros(processed_img.shape, dtype=np.uint8)
#     roi_corners = np.array([[(0, 400), (300, 280), (500, 280), (800, 400), (800, 600), (700, 600), (400, 280),
#                              (180, 600), (0, 600)]], dtype=np.int32)
#     cv2.fillPoly(mask, roi_corners, 255)
#
#     roi = cv2.bitwise_and(processed_img, mask)
#
#     try:
#         lines = cv2.HoughLinesP(roi, 1, np.pi/180, THRESHOLD, np.array([]),minLineLength=300, maxLineGap=150)
#         slope_log = []
#         for line in lines:
#             x1, y1, x2, y2 = line[0]
#             cv2.line(screen, (x1, y1), (x2, y2), (0, 255, 0), 8)
#             slope_log.append(slope(x1, x2, y1, y2))
#     except:
#         pass
#
#     return roi, slope_log

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


def turn_direction(slope_log):
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


def numpy_flip(im):
    """ Most efficient Numpy version as of now. """
    frame = np.array(im, dtype=np.uint8)
    return np.flip(frame[:, :, :3], 2).tobytes()