import cv2
import numpy as np


def merge(bgImg: cv2.Mat, frontImg: cv2.Mat) -> cv2.Mat:
    h, w = bgImg.shape[:2]

    alpha_channel = frontImg[:, :, 3] / 255
    overlay_colors = frontImg[:, :, :3]
    alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

    frontImg = cv2.resize(frontImg, (h, w))
    h, w = frontImg.shape[:2]
    background_subsection = bgImg[0:h, 0:w]

    composite = (
        background_subsection * (1 - alpha_mask) + overlay_colors * alpha_mask
    )

    bgImg[0:h, 0:w] = composite

    # cv2.imwrite("resized_centered.png", bgImg)
    return bgImg
