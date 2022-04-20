from msilib.schema import Error
import cv2 as cv
import click
import glob
import os

import utils.print_img_path as p_print


def do(base_path: str):
    '''Compute the vanishing line based on a selected plane'''

    # Check if the data dir exists
    if not os.path.exists(base_path):
        click.echo(f'Image source path <{base_path}> does not exist')

    # Get all .jpg images from the data folder
    pattern = os.path.join(base_path, '*.jpg')
    img_paths = glob.glob(pattern)

    if len(img_paths) == 0:
        click.echo('No images found. Exiting')
        return

    # Display found images
    click.echo(f'Found <{len(img_paths)}> image(s)')
    p_print.image_list(img_paths)
    input_value = input(f'Enter number between 1 and {len(img_paths)} to select image to use: ')

    # Convert to integer
    index = 0
    try:
        index = int(input_value)
    except:
        click.echo("Invalid input. Exiting")

    # Check if in range
    if index - 1 < 0 or index > len(img_paths):
        raise(IndexError('Invalid index'))

    try:
        img = cv.imread(img_paths[index-1], cv.IMREAD_COLOR)
    except Exception as e:
        print(e)
