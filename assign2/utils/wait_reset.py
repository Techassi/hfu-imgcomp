import cv2 as cv
from cv2 import Mat


def wait_reset(d: int, clicked_points: list[tuple] = None, img_copy: Mat = None, title: str = None):
    '''
    Wait for 'd' milliseconds until we press <q>.
    Or wait for 'd' milliseconds until we press <r>.

    Parameters
    ----------
    d : int
        Delay in milliseconds
    clicked_points : list[tuple]
        Tuple of clicked points
    img_copy : Mat
        A copy of the original, unchanged image
    title : str
        Name of the new window
    '''
    while True:
        img = img_copy.copy()
        key = cv.waitKey(d)

        if key == ord('r'):
            clicked_points.clear()
            img = img_copy.copy()
            cv.imshow(title, img)

        if key == ord('q'):
            return
