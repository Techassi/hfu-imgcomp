import cv2 as cv
import click

import utils.images as images
import utils.input as inp


def do(base_path: str, min: int, max: int):
    '''
    Automatically detect edges in the source image to calculate vanishing line.

    Parameters
    ----------
    base_path : str
        Path to the source image directory
    min : int
        Min value for hysteresis thresholding
    max : int
        Max value for hysteresis thresholding
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

    edges = detect_edges(img_paths[index-1], min, max, True)
    cv.imshow(window_name, edges)
    while True:
        cv.waitKey(10)


def detect_edges(img_path: str, min: int, max: int, grayscale: bool = False) -> any:
    '''
    Detect edges in the input image at 'img_path' with 'min' and 'max'
    hysteresis thresholding. Additionally use the grayscaled version
    of the original image.

    Parameters
    ----------
    img_path : str
        Path of the input image
    min : int
        Min value for hysteresis thresholding
    max : int
        Max value for hysteresis thresholding
    grayscale : bool
        Use grayscaled version of original image

    Returns
    -------
    edges : any
        'Image' of the detected edges
    '''
    img = cv.imread(img_path)

    if grayscale:
        gray_scaled_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        return cv.Canny(gray_scaled_img, min, max, apertureSize=3, L2gradient=True)

    return cv.Canny(img, min, max, apertureSize=3, L2gradient=True)


def detect_lines():
    '''
    Detect continious lines in the input image by using edge detection
    '''
    # TODO (Techassi): Implement this
