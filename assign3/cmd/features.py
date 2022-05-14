from typing import List
import numpy as np
import cv2 as cv
import click

import features.features as features
import utils.drawing as drawing
import utils.images as images
import utils.input as inp


def execute(base_path: str, preview: bool):
    ''''''
    img_paths, ok = images.list(base_path)
    if not ok:
        click.echo('No images found')

    images.print_list(img_paths)

    # Prompt the user to select 2 images
    indices = inp.enforce_multi_range_input(
        f'Enter number between 1 and {len(img_paths)} to select image to use: ', 1, len(img_paths), 3)

    # Collect selected image paths
    selected_img_paths: List[str] = []
    for index in indices:
        selected_img_paths.append(img_paths[index - 1])

    # Load images with OpenCV
    imgs, err = features.load_images(selected_img_paths)
    if err != None:
        click.echo(f'Failed to load images: {err.message}')
        return

    # Get epilines, one function call is just all it takes
    epilines_list = features.get_epilines(imgs)

    for c in epilines_list:
        print(f'Combi: {c[1][0]} with {c[1][1]}')
        print(f'Lines in left {len(c[0][0])}')
        print(f'Lines in right {len(c[0][1])}')
        img1 = drawing.epilines(
            imgs[c[1][1]],
            c[0][0]
        )
        img2 = drawing.epilines(
            imgs[c[1][0]],
            c[0][1]
        )
        cv.namedWindow('preview', cv.WINDOW_NORMAL)
        cv.imshow('preview', np.concatenate((img1, img2), axis=1))
        cv.waitKey(0)
