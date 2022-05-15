from typing import List, Tuple
import cv2 as cv
import click

from thints.images import ImageList
import utils.images as images


def range_input(message: str, min: int, max: int, verbose: bool = True) -> Tuple[int, bool]:
    '''
    Retrieve an integer input between 'min' and 'max' from the user.

    Parameters
    ----------
    message : str
        Message to display for the input prompt
    min : int
        Minimum value of range
    max : int
        Maximum value of range
    verbose : bool
        If status messages should be printed (Default: True)

    Returns
    -------
    value : int
        The input value or -1 when invalid
    ok : bool
        The status of this function
    '''
    input_value = input(message)

    # Convert to integer
    index = -1
    try:
        index = int(input_value)
    except:
        if verbose:
            click.echo('Invalid input. Exiting')
        return (index, False)

    # Check if in range
    if index < min or index > max:
        if verbose:
            click.echo('Invalid index. Out of range. Exiting')
        return (index, False)

    return (index, True)


def enforce_range_input(message: str, min: int, max: int) -> int:
    '''
    Retrieve an integer input between 'min' and 'max' from the user.
    If the user provides an invalid input, try again.

    Parameters
    ----------
    message : str
        Message to display for the input prompt
    min : int
        Minimum value of range
    max : int
        Maximum value of range

    Returns
    -------
    value : int
        The valid input value
    '''
    v, ok = range_input(message, min, max, False)
    while not ok:
        click.echo('Invalid input. Try again')
        v, ok = range_input(message, min, max, False)

    return v


def enforce_multi_range_input(message: str, min: int, max: int, required_inputs: int) -> List[int]:
    '''
    Retrieve multiple integer inputs between 'min' and 'max' from the user.
    If the user provides an invalid input or the provided value is already selected, try again.

    Parameters
    ----------
    message : str
        Message to display for the input prompt
    min : int
        Minimum value of range
    max : int
        Maximum value of range

    Returns
    -------
    values : List[int]
        List of valid input values
    '''
    click.echo(f'A selection of {required_inputs} item(s) is needed\n')

    inputs: List[int] = []
    n = 0

    while n < required_inputs:
        v = enforce_range_input(f'[{n + 1}/{required_inputs}] {message}', min, max)
        if v in inputs:
            click.echo('Already selected. Try again')
            continue

        inputs.append(v)
        n += 1

    return inputs


def handle_images(base_path: str, preview: bool) -> ImageList:
    img_paths, ok = images.list(base_path)
    if not ok:
        click.echo('No images found')

    images.print_list(img_paths)

    # Prompt the use to sepcify how many images to use
    required_inputs = enforce_range_input(
        f'Enter how many images to use (min 2, max {len(img_paths)}): ', 2, len(img_paths))

    # Prompt the user to select n images
    indices = enforce_multi_range_input(
        f'Enter number between 1 and {len(img_paths)} to select image to use: ', 1, len(img_paths), required_inputs)

    # Collect selected image paths
    selected_img_paths: List[str] = []
    for index in indices:
        selected_img_paths.append(img_paths[index - 1])

    # Load images with OpenCV
    imgs, err = images.load_images(selected_img_paths)
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

    return imgs
