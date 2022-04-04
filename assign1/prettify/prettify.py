from typing import Tuple
import numpy as np
import cv2 as cv
import click
import glob
import os

# Local packages
from calibration import calibration
from utils import images, wait

# The code below is based on the OpenCV tutorial on camera calibration available on
# https://docs.opencv.org/4.5.5/dc/dbb/tutorial_py_calibration.html


def do(camera_index: int, base_path: str, results_path: str, live: bool, preview: bool):
    '''Undistort images either in standalone or live mode.

    Args:
        camera_index (int): Camera device index (default 0)
        base_path (str): Base path of source images
        results_path (str): Path in which result images will get saved in standalone mode
        live (bool): Use live mode
        preview (bool): Display preview window
    '''
    click.echo(f'Reading in calibration images from {base_path}')

    # Check if the results dir exists. If not, create it
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    # Get all .jpg images from the data folder
    pattern = os.path.join(base_path, '*.jpg')
    img_paths = glob.glob(pattern)

    click.echo(f'Found {len(img_paths)} image(s)')
    if preview:
        click.echo('Press <n> for next image, <q> to quit')

    # First we get the calibration data with all source images
    click.echo('Calibrating...')
    exit, object_point_list, image_point_list = calibration.get_points(img_paths, preview)
    if exit:
        return

    # Check if the user wants to use live mode
    if live:
        click.echo('Live mode. Prettifying...')
        prettify_live(camera_index, object_point_list, image_point_list)
    else:
        # Prettify the images and save them in the result folder
        click.echo('Standalone mode. Prettifying...')
        prettify_standalone(img_paths, object_point_list, image_point_list, results_path, preview)


def prettify_standalone(img_paths: list, op_list: list, ip_list: list, results_path: str, preview: bool):
    '''Prettify the images using the calibration data.

    Args:
        img_paths (list): List of images to prettify / undistort
        op_list (list): List of object points
        ip_list (list): List of image points
        results_path (str): Path in which prettified images will be saved in
        preview (bool): Display preview window
    '''
    # Take the first image to calibrate the camera
    img, gray_scaled_img = images.read_image_both(img_paths[0])

    # Calibrate the camera
    ok, mtx, dist, rvecs, tvecs, optimized_mtx, roi = calibration.calibrate_camera(
        img, gray_scaled_img, op_list, ip_list)
    if not ok:
        click.echo(f'Failed to calibrate camera with first frame')
        return

    for i in range(len(img_paths)):
        img_path = img_paths[i]

        img = cv.imread(img_path)
        undistorted_img = images.prettify_and_save(img, mtx, dist, optimized_mtx, roi, results_path, i)

        # If the undistortion process failed, continue
        if undistorted_img is None:
            continue

        # Skip preview if --preview is false
        if not preview:
            continue

        # Display preview until we press <n>
        cv.imshow('undistorted', undistorted_img)
        exit = wait.wait(10)
        if exit:
            cv.destroyAllWindows()

        print(f"{len(img_paths) - i - 1} image(s) remaining to view")


def prettify_live(camera_index: int, op_list: list, ip_list: list):
    '''Prettify a live camera feed based on the calibration data

    Args:
        camera_index (int): Camera device index (default 0)
        op_list (list): List of object points
        ip_list (list): List of image points
    '''
    cap = cv.VideoCapture(camera_index)

    # Capture one frame to calculate the gray scaled frame for the shape
    ok, frame = cap.read()
    if not ok:
        return

    gray_scaled_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Calibrate the camera
    ok, mtx, dist, optimized_mtx, roi = calibration.calibrate_camera(frame, gray_scaled_frame, op_list, ip_list)
    if not ok:
        click.echo(f'Failed to calibrate camera with first frame')
        return

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        x, y, w, h = roi
        undistorted_frame = cv.undistort(frame, mtx, dist, None, optimized_mtx)
        undistorted_frame = undistorted_frame[y:y+h, x:x+w]
        cv.imshow('live', undistorted_frame)

        if cv.waitKey(10) == ord('q'):
            break
