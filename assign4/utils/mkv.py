import open3d as o3d
import click
import time

from typing import List, Tuple
import glob
import os

from typings.error import Err, Error
import const


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


def open(
    vid_path: str,
    with_debug: bool = False,
    with_progress: bool = False
) -> Tuple[List[o3d.geometry.RGBDImage], Error]:
    '''
    Open MKV video file with the Open3D AzureKinectMKVReader.

    Parameters
    ----------
    vid_path : str
        Path to MKV video file

    Returns
    -------
    result : Tuple[List[o3d.geometry.RGBDImage], Error]
        List of RGBD images or an error
    '''
    start = time.time()
    reader = o3d.io.AzureKinectMKVReader()

    ok = reader.open(vid_path)
    if not ok:
        return Err('Reader failed to open MKV video file')

    # Retrieve metadata
    meta = reader.get_metadata()
    duration = meta.stream_length_usec * const.USEC_IN_SECONDS
    if with_debug:
        click.echo('Video meta: {}px x {}px ({:.2f}s)'.format(
            meta.width,
            meta.height,
            duration
        ))

    images: List[o3d.geometry.RGBDImage] = []
    processed_images = 0

    with click.progressbar(length=int(duration), label='Reading...') as bar:
        while not reader.is_eof():
            if with_progress and processed_images % 30 == 0 and processed_images != 0:
                bar.update(1)

            images.append(reader.next_frame())
            processed_images += 1

    end = time.time() - start
    if with_progress:
        click.echo('Read {} frame(s) in {:.2f}s ({:.2f}x)'.format(
            processed_images,
            end,
            duration / end
        ))

    return images, None
