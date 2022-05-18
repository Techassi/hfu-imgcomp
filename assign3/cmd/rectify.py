import numpy as np
import cv2 as cv
import click

import geometry.rectification as grect
import features.features as features
import utils.input as inp


def execute(base_path: str, preview: bool, thresh: int):
    imgs, combi_mode, ref_index = inp.handle_images(base_path, preview)
    combis = features.get_combinations(imgs, combi_mode, ref_index)

    click.echo('\nExtracting fundamental matrices. This takes a few seconds...')
    fm_list = features.get_fundamental_matrices(imgs, combis)

    click.echo('Rectifying...')
    rm_list = grect.rectify(imgs, fm_list, thresh)

    cv.namedWindow('rectify', cv.WINDOW_NORMAL)

    for rm in rm_list:
        img_l = cv.warpPerspective(imgs[rm[4][0]], rm[0], rm[2])
        img_r = cv.warpPerspective(imgs[rm[4][1]], rm[1], rm[3])

        cv.imshow('rectify', np.concatenate((img_l, img_r), axis=1))
        cv.waitKey(0)
