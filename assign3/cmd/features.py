from typing import List
import numpy as np
import cv2 as cv
import click

import features.features as features
import utils.drawing as drawing
import utils.images as images
import utils.input as inp


def epilines(base_path: str, preview: bool):
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

    # Show preview if --preview is passed
    if preview:
        cv.namedWindow('preview', cv.WINDOW_NORMAL)
        for img in imgs:
            cv.imshow('preview', img)
            cv.waitKey(0)

        cv.destroyAllWindows()

    # Get epilines, one function call is just all it takes
    click.echo('\nExtracting epilines. This takes a few seconds...\n')
    epilines_list = features.get_epilines(imgs)

    for c in epilines_list:
        click.echo('Showing combination of image {} with image {} with a total of {} lines'.format(
            c[1][0] + 1,
            c[1][1] + 1,
            len(c[0][0])
        ))

        img_left = drawing.epilines(
            imgs[c[1][1]],
            c[0][0]
        )
        img_right = drawing.epilines(
            imgs[c[1][0]],
            c[0][1]
        )

        cv.namedWindow('epilines', cv.WINDOW_NORMAL)
        cv.imshow('epilines', np.concatenate((img_left, img_right), axis=1))
        cv.waitKey(0)

    cv.destroyAllWindows()


def points(base_path: str, preview: bool):
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

    # Get matching points
    click.echo('\nExtracting matching points. This takes a few seconds...\n')
    points_list = features.get_points(imgs)

    for p in points_list:
        click.echo('Showing combination of image {} with image {} with a total of {} points'.format(
            p[4][0] + 1,
            p[4][1] + 1,
            len(p[0])
        ))

        frame = drawing.matching_keypoints(imgs[p[4][0]], p[0], imgs[p[4][1]], p[1], p[2], p[3])
        cv.namedWindow('matches', cv.WINDOW_NORMAL)
        cv.imshow('matches', frame)
        cv.waitKey(0)

    cv.destroyAllWindows()
