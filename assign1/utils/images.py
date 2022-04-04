from typing import Tuple
import cv2 as cv
import os


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


def prettify_and_save(img: any, mtx: any, dist: any, optimized_mtx: any, roi: any, results_path: str, idx: int) -> any:
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
    x, y, w, h = roi
    undistorted_img = cv.undistort(img, mtx, dist, None, optimized_mtx)
    undistorted_img = undistorted_img[y:y+h, x:x+w]

    # Save image
    p = os.path.join(results_path, f"img{idx}.jpg")
    cv.imwrite(p, undistorted_img)

    return undistorted_img
