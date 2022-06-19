import open3d as o3d
import click
import glob
import os

import utils.images as imgop
import utils.input as inp


def execute(base_path: str, config_path: str):
    # Set verbosity level to only errors
    o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Warning)

    # Check if there are already images present, if yes ask if the user wants to overide
    imgs = glob.glob(os.path.join(base_path, 'image', '*.jpg'))
    if len(imgs) > 0 and not inp.confirmation_prompt('Extracted images detected. Overide?', default=False):
        return

    # Handle MKV video file selection and reading
    images, err = inp.handle_mkv_files(base_path)
    if err != None:
        click.echo(err.message)
        return

    # Split the list of RGBD image into two lists of RGB and depth images
    color_images, depth_images = imgop.split_rgbd_image_into_parts(images)

    # Save images
    err = imgop.save_split_images(base_path, color_images, depth_images)
    if err != None:
        click.echo(err.message)
        return
