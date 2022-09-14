import base64
from typing import BinaryIO

import cv2
import numpy as np

from app.utils.image import merge

from .config import getCover


def mergeImage(f: bytes) -> bytes:
    bgImg = cv2.imdecode(np.frombuffer(f, np.int8), cv2.IMREAD_COLOR)

    return_img = merge(bgImg, getCover())

    _, encoded_img = cv2.imencode(".PNG", return_img)
    encoded_img = base64.b64encode(encoded_img)

    return encoded_img
