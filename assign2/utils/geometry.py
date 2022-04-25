from typing import Tuple
import numpy as np


def line_from(a: tuple, b: tuple) -> np.ndarray:
    '''
    Calculate a line between two points.

    Parameters
    ----------
    a : list
        The first point as a list of x, y coordinates.
    b : list
        The second point as a list of x, y coordinates.

    Returns
    -------
    line : np.ndarray
        The line through both points.
    '''
    return np.cross((a[0], a[1], 1), (b[0], b[1], 1))


def intersection_from(a: np.ndarray, b: np.ndarray) -> Tuple[int, int]:
    '''
    Calculate the intersection position of two lines.

    Parameters
    ----------
    a : np.ndarray
        The first line.
    b : np.ndarray
        The second line.

    Returns
    -------
    pos : Tuple[int, int]
        The intersection postion as x, y coordinates
    '''
    pos = np.cross(a, b)
    pos = pos / pos[2]
    return (round(pos[0]), round(pos[1]))
