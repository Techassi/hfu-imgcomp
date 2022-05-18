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


def enforce_input_from_values(message: str, values: List[int]) -> int:
    ''''''
    index = -1
    while True:
        input_value = input(message)

        try:
            index = int(input_value)
        except:
            click.echo('Invalid input. Please retry')
            continue

        if index not in values:
            click.echo('Selected value not in List of allowed values. Please retry')
            continue

        break

    return index


def handle_images(base_path: str, preview: bool) -> Tuple[ImageList, int, int]:
    ''''''
    img_paths, ok = images.list(base_path)
    if not ok:
        click.echo('No images found')

    # Prompt the user to sepcify how many images to use
    required_inputs = enforce_range_input(
        f'Enter how many images to use (min 2, max {len(img_paths)}): ', 2, len(img_paths))

    # Prompt the user to specify which combinations to create
    combi_mode = handle_combination_mode()

    images.print_list(img_paths)

    # Prompt the user to select n images
    indices = enforce_multi_range_input(
        f'Enter number between 1 and {len(img_paths)} to select image to use: ', 1, len(img_paths), required_inputs)

    # If the user selected the ref combination mode, aks for the index of the reference image
    ref_index = -1
    if combi_mode == 2:
        allowed_indices = [i for i in range(1, len(indices) + 1)]
        ref_index = enforce_input_from_values('Please enter the index of the reference image: ', allowed_indices)

    # Collect selected image paths
    selected_img_paths: List[str] = []
    for index in indices:
        selected_img_paths.append(img_paths[index - 1])

    # Load images with OpenCV
    imgs, err = images.load_images(selected_img_paths)
    if err != None:
        click.echo(f'Failed to load images: {err.message}')
        return None, combi_mode, ref_index

    # Show preview if --preview is passed
    if preview:
        cv.namedWindow('preview', cv.WINDOW_NORMAL)
        for img in imgs:
            cv.imshow('preview', img)
            cv.waitKey(0)

        cv.destroyAllWindows()

    # Return ref_index - 1 as this value is not zero-indexed
    return imgs, combi_mode, ref_index - 1


def handle_combination_mode() -> int:
    click.echo('\nPlease select the combination mode')
    click.echo('-------')
    click.echo('  [1] All combinations\n  [2] All combinations with a reference image')
    click.echo('-------')

    return enforce_range_input('Enter a number between 1 and 2: ', 1, 2)
