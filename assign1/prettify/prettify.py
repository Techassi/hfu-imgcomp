from typing import Tuple
import numpy as np
import cv2 as cv
import click
import glob
import os


'''The code below is based on the OpenCV tutorial on camera calibration 
available under https://docs.opencv.org/4.5.5/dc/dbb/tutorial_py_calibration.html'''


def do(base_path: str, results_path: str):
    '''Undistort live image from a camera'''
    click.echo(f'Reading in calibration images from {base_path}')

    # Check if the results dir exists. If not, create it
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    # Get all .jpg images from the data folder
    pattern = os.path.join(base_path, '*.jpg')
    img_paths = glob.glob(pattern)

    click.echo(f'Found {len(img_paths)} image(s)')
    click.echo('Press <n> for next image')

    # Numpy magic
    object_points = np.zeros((9*6, 3), np.float32)
    object_points[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

    object_point_list = []
    image_point_list = []

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

        # Draw and display detected corners for all images
        cv.drawChessboardCorners(img, (9, 6), optimized_corners, ok)
        cv.imshow('img', img)

        # Display preview until we press <n>
        exit = wait(10)
        if exit:
            break

        print(f"{len(img_paths) - i - 1} image(s) remaining to view")

        # Prettify the image and save it in the result folder
        prettify_image(img, gray_scaled_img, object_point_list, image_point_list, results_path, i)

    cv.destroyAllWindows()


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


def prettify_image(img: any, gray: any, opl: list, ipl: list, results_path: str, i: int):
    '''Prettify image and save it'''
    # Calibrate the camera
    ok, mtx, dist, rvecs, tvecs = cv.calibrateCamera(opl, ipl, gray.shape[::-1], None, None)
    if not ok:
        click.echo(f'Failed to calibrate camera with img{i}.jpg')
        return

    # Undistort
    undistorted_img = cv.undistort(img, mtx, dist, None)

    # Save image
    p = os.path.join(results_path, f"img{i}.jpg")
    cv.imwrite(p, undistorted_img)


def wait(d: int) -> bool:
    '''Wait for <d> milliseconds and return if we want to exit'''
    while True:
        key = cv.waitKey(d)
        if key == ord('n'):
            return False

        if key == ord('q'):
            return True
