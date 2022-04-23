import cv2 as cv


def wait(d: int):
    '''
    Wait for 'd' milliseconds until we press <q>.

    Parameters
    ----------
    d : int
        Delay in milliseconds
    '''
    while True:
        key = cv.waitKey(d)
        if key == ord('q'):
            return
