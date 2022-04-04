from typing import Tuple
import numpy as np
import cv2 as cv
import click
import glob
import os

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
    exit, object_point_list, image_point_list = get_calibration_data(img_paths, preview)
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


def get_calibration_data(img_paths: list, preview: bool) -> Tuple[bool, list, list]:
    '''Find chessboard corners using the source images. This function returns a triple.

    Args:
        img_paths (list): List of source image paths
        preview (bool): Display preview window

    Returns:
        exit (bool): This indicates if the user wants to exit (by pressing q)
        object_point_list (list): List of object points
        image_point_list (list): List of image points
    '''
    object_point_list = []
    image_point_list = []

    # Numpy magic
    object_points = np.zeros((9*6, 3), np.float32)
    object_points[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

    # Iterate over all found images
    for i in range(len(img_paths)):
        img_path = img_paths[i]

        # Read in image
        img, gray_scaled_img = read_image_both(img_path)

        # Find corners
        ok, corners, optimized_corners = find_corners(gray_scaled_img)
        if not ok:
            click.echo(f'Failed to find corners in {img_path}')
            continue

        object_point_list.append(object_points)
        image_point_list.append(corners)

        # Skip preview if --preview is false
        if not preview:
            continue

        # Draw and display detected corners for all images
        cv.drawChessboardCorners(img, (9, 6), optimized_corners, ok)
        cv.imshow('img', img)

        # Display preview until we press <n>
        exit = wait(10)
        if exit:
            cv.destroyAllWindows()
            return True, object_point_list, image_point_list

        print(f"{len(img_paths) - i - 1} image(s) remaining to view")

    return False, object_point_list, image_point_list


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
    gray_scaled_img = read_image_gray(img_paths[0])

    # Calibrate the camera
    ok, mtx, dist, rvecs, tvecs = cv.calibrateCamera(op_list, ip_list, gray_scaled_img.shape[::-1], None, None)
    if not ok:
        click.echo(f'Failed to calibrate camera with first frame')
        return

    for i in range(len(img_paths)):
        img_path = img_paths[i]

        img = cv.imread(img_path)
        undistorted_img = prettify_and_save_image(img, mtx, dist, results_path, i)

        # If the undistortion process failed, continue
        if undistorted_img is None:
            continue

        # Skip preview if --preview is false
        if not preview:
            continue

        # Display preview until we press <n>
        cv.imshow('undistorted', undistorted_img)
        exit = wait(10)
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
    # TODO (Techassi): Add matrix optimizations, see cv.getOptimalNewCameraMatrix()
    # TODO (Techassi): Move the calibration and optimization code into a function
    ok, mtx, dist, rvecs, tvecs = cv.calibrateCamera(op_list, ip_list, gray_scaled_frame.shape[::-1], None, None)
    if not ok:
        click.echo(f'Failed to calibrate camera with first frame')
        return

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        undistorted_frame = cv.undistort(frame, mtx, dist, None)
        cv.imshow('live', undistorted_frame)

        if cv.waitKey(10) == ord('q'):
            break


def read_image_both(img_path: str) -> Tuple[any, any]:
    '''Read in image at <img_path> and return the original and gray scaled version of it.

    Args:
        img_path (str): Path to image

    Returns:
        img (any): Original image
        gray_scaled_img (any): Gray scaled image
    '''
    img = cv.imread(img_path)
    gray_scaled_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    return img, gray_scaled_img


def read_image_gray(img_path: str) -> any:
    '''Read in image at <img_path> and return the gray scaled version of it.

    Args:
        img_path (str): Path to image

    Returns:
        gray_scaled_img (any): Gray scaled image
    '''
    img = cv.imread(img_path)
    gray_scaled_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return gray_scaled_img


def find_corners(gray_scaled_img: any) -> Tuple[bool, list, list]:
    '''Find chessboard corners in gray scaled image

    Args:
        gray_scaled_image (any): The gray scaled input image

    Returns:
        ok (bool): If successfull True, otherwise False
        corners (list): List of found corners
        optimized_corners (list): List of optimized corners
    '''
    ok, corners = cv.findChessboardCorners(gray_scaled_img, (9, 6), None)
    if not ok:
        return False, [], []

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    optimized_corners = cv.cornerSubPix(gray_scaled_img, corners, (11, 11), (-1, -1), criteria)

    return True, corners, optimized_corners


def prettify_and_save_image(img: any, mtx: any, dist: any, results_path: str, idx: int) -> any:
    '''Prettify image and save it inside <results_path>

    Args:
        img (any): Input (original) image
        mtx (any): Camera matrix
        dist (any): Distortion coefficients
        results_path (str): Path in which prettified images will be saved in
        idx (int): Index of the current image

    Returns:
        undistorted_img (any): Undistorted image
    '''
    # Undistort
    undistorted_img = cv.undistort(img, mtx, dist, None)

    # Save image
    p = os.path.join(results_path, f"img{idx}.jpg")
    cv.imwrite(p, undistorted_img)

    return undistorted_img


def wait(d: int) -> bool:
    '''Wait for <d> milliseconds and return if we want to exit

    Args:
        d (int): Delay in milliseconds

    Returns:
        exit (bool): True if the user wants to exit, otherwise False
    '''
    while True:
        key = cv.waitKey(d)
        if key == ord('n'):
            return False

        if key == ord('q'):
            return True
