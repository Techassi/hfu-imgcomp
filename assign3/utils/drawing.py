from typing import List, Tuple
import numpy as np
import cv2 as cv


def epilines(img, lines):
    ''''''
    # NOTE (Techassi): I dunno what the hell is going on here, so I just blatantly copied this :)
    r, c = img.shape
    img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    for r in lines:
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r[2]/r[1]])
        x1, y1 = map(int, [c, -(r[2]+r[0]*c)/r[1]])
        img = cv.line(img, (x0, y0), (x1, y1), color, 1)
    return img


def matching_keypoints(
    img_l: cv.Mat,
    kp_l: List[cv.KeyPoint],
    img_r: cv.Mat,
    kp_r: List[cv.KeyPoint],
    matches: Tuple[Tuple[cv.DMatch, cv.DMatch]],
    mask: List[List[int]]
) -> cv.Mat:
    '''
    Draw connecting lines for matched points.
    '''
    params = dict(
        flags=cv.DrawMatchesFlags_DEFAULT,
        singlePointColor=(255, 0, 0),
        matchColor=(0, 255, 0),
        matchesMask=mask
    )
    return cv.drawMatchesKnn(img_l, kp_l, img_r, kp_r, matches, None, **params)
