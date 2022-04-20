import cv2 as cv
import click
import glob
import os

import utils.wait as wait
import utils.fmt as fmt


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
    fmt.print_image_list(img_paths)
    input_value = input(f'Enter number between 1 and {len(img_paths)} to select image to use: ')

    # Convert to integer
    index = 0
    try:
        index = int(input_value)
    except:
        click.echo('Invalid input. Exiting')
        return

    # Check if in range
    if index - 1 < 0 or index > len(img_paths):
        click.echo('Invalid index. Out or range. Exiting')
        return

    # try:
    #     img = cv.imread(img_paths[index-1], cv.IMREAD_COLOR)
    # except Exception as e:
    #     print(e)

    img = cv.imread(img_paths[index-1])
    cv.imshow('win', img)

    exit = wait.wait(10)
    if exit:
        return
