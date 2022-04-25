import cv2 as cv


def circle(img, x: int, y: int, color: tuple = (0, 0, 0), window_name: str = 'win'):
    '''
    Draw circle in 'img' at 'x' and 'y' with 'color'.

    Parameters
    ----------
    img : Mat
        Image matrix
    x : int
        X position
    y : int
        Y position
    color : tuple
        Color of the circle (Default 0, 0, 0)
    '''
    cv.circle(img, (x, y), 5, color, 10)
    cv.imshow(window_name, img)


def line(img, a: tuple, b: tuple, color: tuple = (244, 164, 96), window_name: str = 'win'):
    '''
    Draw a line between two points 'a' and 'b' with 'color'.

    Parameters
    ----------
    img : Mat
        Image matrix
    a : tuple
        First point
    b : tuple
        Second point
    color : tuple
        Color of the line (Default 244, 164, 96)
    '''
    cv.line(img, a, b, color, 5)
    cv.imshow(window_name, img)
