from typing import List
import cv2 as cv
import click

import features.features as features
import utils.images as images
import utils.input as inp
import utils.wait as wait


def execute(base_path: str, preview: bool):
    ''''''
    img_paths, ok = images.list(base_path)
    if not ok:
        click.echo('No images found')

    images.print_list(img_paths)

    # Prompt the user to select 2 images
    indices = inp.enforce_multi_range_input(
        f'Enter number between 1 and {len(img_paths)} to select image to use: ', 1, len(img_paths), 2)

    # Collect selected image paths
    selected_img_paths: List[str] = []
    for index in indices:
        selected_img_paths.append(img_paths[index - 1])

    # Load images with OpenCV
    imgs, err = features.load_images(selected_img_paths)
    if err != None:
        click.echo(f'Failed to load images: {err.message}')
        return

    keypoints_descriptor_list = features.get_keypoints(imgs)
    flann_matches_list = features.match_keypoints(keypoints_descriptor_list)
    filtered_matches_list = features.filter_matches(keypoints_descriptor_list, flann_matches_list)

    # for i, combi in enumerate(keypoints_descriptor_list):
    #     print('We found {} keypoints in the first image and {} keypoints in the second image'.format(
    #         len(combi[0][0]),
    #         len(combi[0][1]))
    #     )

    #     if preview:
    #         # Visualize the found points in a preview window
    #         cv.namedWindow('preview', cv.WINDOW_NORMAL)
    #         img_with_points = cv.drawKeypoints(
    #             imgs[i],
    #             combi[0][0],
    #             None,
    #             flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    #         )
    #         cv.imshow('preview', img_with_points)
    #         if wait.wait_or(0):
    #             continue
