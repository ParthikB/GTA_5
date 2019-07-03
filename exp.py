import numpy as np
import cv2


data = np.load("1.npy")

for screen in data:
    # time.sleep(0.1)
    img = screen[0]
    cv2.imshow("test", img)
    print(screen[1])
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

# print(data[0][0].shape)