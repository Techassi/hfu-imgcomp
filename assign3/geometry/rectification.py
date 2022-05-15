import cv2 as cv

from thints.geometry import RectificationMatricesList
from thints.features import FundamentalMatricesList
from thints.images import ImageList


def rectify(imgs: ImageList, fm_list: FundamentalMatricesList, thresh: int = 0) -> RectificationMatricesList:
    ''''''
    matrices_list: RectificationMatricesList = []

    for m in fm_list:
        img_height_l, img_width_l = imgs[m[4][0]].shape
        img_height_r, img_width_r = imgs[m[4][1]].shape

        _, h_l, h_r = cv.stereoRectifyUncalibrated(m[2], m[3], m[0], (img_width_l, img_height_l), threshold=thresh)
        matrices_list.append(
            (
                h_l,
                h_r,
                (img_height_l, img_width_l),
                (img_height_r, img_width_r),
                m[4]
            )
        )

    return matrices_list
