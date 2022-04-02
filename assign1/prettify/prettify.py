from typing import Tuple
import cv2 as cv
import click
import glob
import os


def do(path: str):
    '''Undistort live image from a camera'''
    click.echo(f'Reading in calibartion images from {path}')

    pattern = os.path.join(path, '*.jpg')
    img_paths = glob.glob(pattern)
    img_counter = len(img_paths)
    click.echo(f'Found {len(img_paths)} image(s)')

    for img_path in img_paths:
        img_counter -= 1
        ok, corners, img = find_corners(img_path)
        if not ok:
            click.echo(f'Failed to find corners in {img_path}')
            continue

        cv.drawChessboardCorners(img, (9, 6), corners, ok)
        cv.imshow('img', img)

        while True:
            if cv.waitKey(10) == ord('n'):
                print(f"{img_counter} image(s) remaining to view")
                break

    cv.destroyAllWindows()


def find_corners(img_path: str) -> Tuple[bool, list, any]:
    '''Read in image and find chessboard corners'''
    img = cv.imread(img_path)
    gray_scaled_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ok, corners = cv.findChessboardCorners(gray_scaled_img, (9, 6), None)
    if not ok:
        return False, [], None

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    optimized_corners = cv.cornerSubPix(gray_scaled_img, corners, (11, 11), (-1, -1), criteria)

    return True, optimized_corners, img
