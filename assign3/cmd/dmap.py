import numpy as np
import cv2 as cv
import click

import geometry.geometry as geometry
import features.features as features
import utils.input as inp


def single(base_path: str, preview: bool):
    imgs = inp.handle_images(base_path, preview)

    click.echo('\nExtracting fundamental matrices. This takes a few seconds...\n')

    fm_list = features.get_fundamental_matrices(imgs)
    rm_list = geometry.rectify(imgs, fm_list)

    cv.namedWindow('depth-map', cv.WINDOW_NORMAL)

    for rm in rm_list:
        img_l = cv.warpPerspective(imgs[rm[4][0]], rm[0], rm[2])
        img_r = cv.warpPerspective(imgs[rm[4][1]], rm[1], rm[3])

        cv.imshow('depth-map', np.concatenate((img_l, img_r), axis=1))
        cv.waitKey(0)
