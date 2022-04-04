from typing import Tuple
import numpy as np
import cv2 as cv
import click

from utils import images, wait


def get_points(img_paths: list, preview: bool) -> Tuple[bool, list, list]:
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
        img, gray_scaled_img = images.read_image_both(img_path)

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
        exit = wait.wait(10)
        if exit:
            cv.destroyAllWindows()
            return True, object_point_list, image_point_list

        print(f"{len(img_paths) - i - 1} image(s) remaining to view")

    return False, object_point_list, image_point_list


def find_corners(gray_scaled_img: any) -> Tuple[bool, list, list]:
    '''Find chessboard corners in gray scaled image

    Args:
        gray_scaled_image (any): The gray scaled input image

    Returns:
        ok (bool): If successful True, otherwise False
        corners (list): List of found corners
        optimized_corners (list): List of optimized corners
    '''
    ok, corners = cv.findChessboardCorners(gray_scaled_img, (9, 6), None)
    if not ok:
        return False, [], []

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    optimized_corners = cv.cornerSubPix(gray_scaled_img, corners, (11, 11), (-1, -1), criteria)

    return True, corners, optimized_corners


def calibrate_camera(img: any, gray_scaled_img: any, op_list: list, ip_list: list) -> Tuple[bool, any, any, any, any]:
    '''Calibrate the camera and optimize the camera matrix. The optimized matrix can bes used to undistort the image.

    Args:
        img (any): The original image
        gray_scaled_img (any): The gray scaled image
        op_list (list): List of object points
        ip_list (list): List of image points

    Returns:
        ok (bool): True if successful, otherwise False
        mtx (any): Camera matrix
        dist (any): Distortion coefficients
        optimized_mtx (any): Optimized (new) camera matrix
        roi (any): Region of interest (x, y, w, h)
    '''
    # Calibrate the camera
    ok, mtx, dist, rvecs, tvecs = cv.calibrateCamera(op_list, ip_list, gray_scaled_img.shape[::-1], None, None)
    if not ok:
        click.echo('Failed to calibrate camera')
        return False, None, None, None, None

    height, width = img.shape[:2]
    optimized_mtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))

    print(roi)

    return True, mtx, dist, optimized_mtx, roi
