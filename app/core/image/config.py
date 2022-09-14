import os

import cv2


def getCover() -> cv2.Mat:
    path = os.getcwd() + "/asset/cover.png"
    return cv2.imread(path, cv2.IMREAD_UNCHANGED)
