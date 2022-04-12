from typing import Tuple
import numpy as np


def get_line_from(a: list, b: list) -> np.ndarray:
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
    return np.cross(a, b)


def get_intersection_pos(a: np.ndarray, b: np.ndarray) -> Tuple[int, int]:
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
