import open3d as o3d
import click

from typings.error import Err, Error

from typing import Tuple, List
import utils.mkv as mkv


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
    input_value = input('{}: '.format(message))

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

    click.echo('\n')
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


def handle_mkv_files(base_path: str) -> Tuple[List[o3d.geometry.RGBDImage], Error]:
    '''
    Handle the globbing, display, selection and reading process of MKV video files.

    Parameters
    ----------
    base_path : str
        Base video file source path

    Returns
    -------
    result : Tuple[List[o3d.geometry.RGBDImage], Error]
        List of RGBD images or an error
    '''
    # Get list of video paths
    vid_paths, ok = mkv.list(base_path)
    if not ok:
        return [], Err('Failed to glob .mkv video files')

    # Print list of video paths
    mkv.print_list(vid_paths)

    # Let the user select the video he wants to use
    index = enforce_range_input(
        'Please select a video file to use',
        1, len(vid_paths)
    )

    # Read every RGBD frame
    images, err = mkv.open(vid_paths[index - 1], with_debug=True, with_progress=True)
    if err != None:
        return [], err

    return images, None
