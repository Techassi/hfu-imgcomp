import cv2 as cv
import click
import glob
import os

import prettify.prettify as prettify

# The reprojection error code is taken from https://docs.opencv.org/4.5.5/dc/dbb/tutorial_py_calibration.html


def do(base_path: str, preview: bool):
    '''Print the reprojection error.

    Args:
        base_path (str): Base path of source images
        preview (bool): Display preview window    
    '''
    click.echo(f'Reading in calibration images from {base_path}')

    # Get all .jpg images from the data folder
    pattern = os.path.join(base_path, '*.jpg')
    img_paths = glob.glob(pattern)

    exit, op_list, ip_list = prettify.get_calibration_data(img_paths, preview)
    if exit:
        return

    # Take the first image to calibrate the camera
    gray_scaled_img = prettify.read_image_gray(img_paths[0])

    ok, mtx, dist, rvecs, tvecs = cv.calibrateCamera(op_list, ip_list, gray_scaled_img.shape[::-1], None, None)
    if not ok:
        click.echo(f'Failed to calibrate camera with {img_paths[0]}')
        return

    # Calculate the reprojection error
    mean_error = 0
    for i in range(len(op_list)):
        img_points, _ = cv.projectPoints(op_list[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv.norm(ip_list[i], img_points, cv.NORM_L2)/len(img_points)
        mean_error += error

    click.echo(f"Total error: {mean_error/len(op_list)}")