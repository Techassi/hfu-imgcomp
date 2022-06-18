import click

from typing import Tuple
import glob
import os


def list(base_path: str) -> Tuple[list, bool]:
    '''
    Return a list of .mkv file paths.

    Parameters
    ----------
    base_path : str
        MKV video base path

    Returns
    -------
    img_paths : list
        List of found .mkv file paths
    ok : bool
        Status of this function
    '''
    # Check if the data dir exists
    if not os.path.exists(base_path):
        return ([], False)

    # Get all .mkv videos from the data folder
    pattern = os.path.join(base_path, '*.mkv')
    vid_paths = glob.glob(pattern)

    # No videos found
    if len(vid_paths) == 0:
        return ([], False)

    return (vid_paths, True)


def print_list(vid_paths: list):
    '''
    Print a list of video files.

    Parameters
    ----------
    vid_paths : list
        List of video file paths
    '''
    sep = '------------------' + ('-' * (len(vid_paths) // 10))
    click.echo(f'\nFound <{len(vid_paths)}> video(s)\n{sep}')

    for i in range(len(vid_paths)):
        vid_path = vid_paths[i]
        click.echo(f"  [{i+1}] {vid_path}")

    click.echo(sep)
