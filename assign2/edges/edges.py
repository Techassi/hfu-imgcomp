import cv2 as cv
import click

import utils.images as images
import utils.input as inp
import utils.wait as wait


def do(base_path: str, max: int, min: int):
    '''
    Automatically detect edges in the source image to calculate vanishing line.

    Parameters
    ----------
    base_path : str
        Path to the source image directory
    max : int
        Max value for hysteresis thresholding
    min : int
        Min value for hysteresis thresholding
    '''
    window_name = 'win'

    # Glob images
    img_paths, ok = images.list(base_path)
    if not ok:
        return

    # Display found images
    click.echo(f'Found <{len(img_paths)}> image(s)')
    images.print_list(img_paths)

    index = inp.enforce_range_input(
        f'Enter number between 1 and {len(img_paths)} to select image to use: ', 1, len(img_paths))

    img = cv.imread(img_paths[index-1])
    cv.imshow(window_name, img)

    wait.wait(10)
