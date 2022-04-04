import cv2 as cv


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
