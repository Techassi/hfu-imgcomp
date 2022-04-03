from curses import echo
from typing import Tuple
import numpy as np
import cv2 as cv
import click
import glob
import os


def do(camera_index: int, base_path: str, results_path: str, live: bool, preview: bool):
    '''Undistort live image from a camera'''
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

    object_point_list = []
    image_point_list = []

    # First we calibrate with all source images
    click.echo('Calibrating...')
    exit = calibrate(img_paths, object_point_list, image_point_list, preview)
    if exit:
        return

    # Check if the user wants to use live mode
    if live:
        click.echo('Live mode. Prettifying...')
        prettify_live(camera_index, object_point_list, image_point_list)
    else:
        # Prettify the images and save them in the result folder
        click.echo('Standalone mode. Prettifying...')
        prettify(img_paths, object_point_list, image_point_list, results_path, preview)


def calibrate(img_paths: list, object_point_list: list, image_point_list: list, preview: bool) -> bool:
    '''Calibrate using the source images'''
    # Numpy magic
    object_points = np.zeros((9*6, 3), np.float32)
    object_points[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

    # Iterate over all found images
    for i in range(len(img_paths)):
        img_path = img_paths[i]

        # Read in image
        img, gray_scaled_img = read_image(img_path)

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
            return True

        print(f"{len(img_paths) - i - 1} image(s) remaining to view")


def prettify(img_paths: list, object_point_list: list, image_point_list: list, results_path: str, preview: bool):
    '''Prettify the images using the calibration data'''
    for i in range(len(img_paths)):
        img_path = img_paths[i]

        img, gray_scaled_img = read_image(img_path)
        undistorted_img = prettify_image(img, gray_scaled_img, object_point_list, image_point_list, results_path, i)

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
    cap = cv.VideoCapture(camera_index)

    # Capture one frame to calculate the gray scaled frame for the shape
    ok, frame = cap.read()
    if not ok:
        return

    gray_scaled_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Calibrate the camera
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


def read_image(img_path: str) -> Tuple[any, any]:
    '''Read in image and return the orignial and gray scaled one'''
    img = cv.imread(img_path)
    gray_scaled_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    return img, gray_scaled_img


def find_corners(gray_scaled_img: any) -> Tuple[bool, list, list]:
    '''Read in image and find chessboard corners'''

    ok, corners = cv.findChessboardCorners(gray_scaled_img, (9, 6), None)
    if not ok:
        return False, [], []

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    optimized_corners = cv.cornerSubPix(gray_scaled_img, corners, (11, 11), (-1, -1), criteria)

    return True, corners, optimized_corners


def prettify_image(img: any, gray: any, op_list: list, ip_list: list, results_path: str, i: int) -> any:
    '''Prettify image and save it'''
    # Calibrate the camera
    ok, mtx, dist, rvecs, tvecs = cv.calibrateCamera(op_list, ip_list, gray.shape[::-1], None, None)
    if not ok:
        click.echo(f'Failed to calibrate camera with img{i}.jpg')
        return None

    # Undistort
    undistorted_img = cv.undistort(img, mtx, dist, None)

    # Save image
    p = os.path.join(results_path, f"img{i}.jpg")
    cv.imwrite(p, undistorted_img)

    return undistorted_img


def wait(d: int) -> bool:
    '''Wait for <d> milliseconds and return if we want to exit'''
    while True:
        key = cv.waitKey(d)
        if key == ord('n'):
            return False

        if key == ord('q'):
            return True
