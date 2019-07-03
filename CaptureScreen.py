import mss.tools
import numpy as np


with mss.mss() as sct:
    # start = time.time()
    monitor = {"top": 32, "left": 1119, "width": 800, "height": 600}
    sct_img = sct.grab(monitor)
    screen = np.array(sct_img)