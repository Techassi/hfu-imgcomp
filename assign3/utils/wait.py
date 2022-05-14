import cv2 as cv


def wait_or(d: int, key: str = 'q') -> bool:
    code = cv.waitKey(d)
    if code == ord(key):
        return True

    return False
