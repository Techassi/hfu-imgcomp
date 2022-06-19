import open3d as o3d
import click
import os

from typings.error import Error, Err
from typing import List, Tuple


def split_rgbd_image_into_parts(
    images: List[o3d.geometry.RGBDImage]
) -> Tuple[List[o3d.geometry.Image], List[o3d.geometry.Image]]:
    '''
    Split up the list of RGBD images into two lists consiting of RGB and depth images.

    Parameters
    ----------
    images : List[o3d.geometry.RGBDImage]
        List of RGBD images

    Returns
    -------
    result : Tuple[List[o3d.geometry.Image], List[o3d.geometry.Image]]
        Two separate lists of RGB and depth images
    '''
    color_images: List[o3d.geometry.Image] = []
    depth_images: List[o3d.geometry.Image] = []

    for image in images:
        color_images.append(image.color)
        depth_images.append(image.depth)

    return color_images, depth_images


def save_split_images(
    base_path: str,
    color_images: List[o3d.geometry.Image],
    depth_images: List[o3d.geometry.Image]
) -> Error:
    ''''''
    # Check if both lists are equally sized
    if len(color_images) != len(depth_images):
        return Err('Length of image lists don\'t match')

    # Check if the required 'image' and 'depth' folders exist
    color_image_base_path = os.path.join(base_path, 'image')
    depth_image_base_path = os.path.join(base_path, 'depth')

    if not os.path.exists(color_image_base_path):
        os.mkdir(color_image_base_path)

    if not os.path.exists(depth_image_base_path):
        os.mkdir(depth_image_base_path)

    # Save images
    with click.progressbar(length=len(color_images), label='Writing...') as bar:
        for i in range(0, len(color_images)):
            if not color_images[i] or not depth_images[i]:
                continue

            color_image_path = os.path.join(color_image_base_path, '{:04d}.jpg'.format(i))
            depth_image_path = os.path.join(depth_image_base_path, '{:04d}.png'.format(i))

            ok = o3d.io.write_image(color_image_path, color_images[i])
            if not ok:
                return Err('Failed to write color JPG image (Frame {:04d})'.format(i))

            ok = o3d.io.write_image(depth_image_path, depth_images[i])
            if not ok:
                return Err('Failed to write depth PNG image (Frame {:04d})'.format(i))

            bar.update(1)

    return None
