from typing import List, Tuple
import cv2 as cv
import click
import glob
import os

from thints.images import ImageList


class ImageError:
    def __init__(self, message: str) -> None:
        self.message = message


def list(base_path: str) -> Tuple[list, bool]:
    '''
    Return a list of image paths

    Parameters
    ----------
    base_path : str
        Image source base path

    Returns
    -------
    img_paths : list
        List of found image paths
    ok : bool
        Status of this function
    '''
    # Check if the data dir exists
    if not os.path.exists(base_path):
        return ([], False)

    # Get all .jpg images from the data folder
    pattern = os.path.join(base_path, '*.jpg')
    img_paths = glob.glob(pattern)

    # No images found
    if len(img_paths) == 0:
        return ([], False)

    return (img_paths, True)


def print_list(img_paths: list):
    '''
    Print a list of images.

    Parameters
    ----------
    img_paths : list
        List of image paths
    '''
    sep = '------------------' + ('-' * (len(img_paths) // 10))
    click.echo(f'Found <{len(img_paths)}> image(s)\n{sep}')

    for i in range(len(img_paths)):
        img_path = img_paths[i]
        click.echo(f"  [{i+1}] {img_path}")

    click.echo(sep)


def load_images(paths: List[str]) -> Tuple[ImageList, ImageError]:
    '''
    Load n images from 'paths' via OpenCV at the same time in grayscale.

    Parameters
    ----------
    paths : List[str]
        List of image paths

    Returns
    -------
    result : Tuple[ImageList, FeaturesError]
        List of images (matrices) or an error
    '''
    images = []

    for path in paths:
        if not os.path.exists(path):
            return images, ImageError(f'Image at {path} does not exist')

        try:
            img = cv.imread(path, cv.IMREAD_GRAYSCALE)
            images.append(img)
        except:
            return images, ImageError(f'Failed to read image at {path}')

    return images, None
