from typing import Dict, Tuple
from io import BufferedReader

import numpy as np
import exifread

import utils.utils as utils


class ExifError:
    def __init__(self, message: str) -> None:
        self.message = message


def read(path: str) -> Tuple[Dict[str, any], ExifError]:
    '''
    Read EXIF data from an image at 'path'.

    Parameters
    ----------
    path : str
        Path to the image

    Returns
    -------
    result : Tuple[Dict[str, any], ExifError]
        A result tuple consisting of the found tags or an error
    '''
    f: BufferedReader = None
    try:
        f = open(path, 'rb')
    except:
        return None, ExifError('Failed to open image')

    tags = exifread.process_file(f)

    try:
        f.close()
    except:
        return None, ExifError('Failed to close file handle')

    return tags, None


def get(key: str, tags: Dict[str, any], is_numeric: bool = False, dtype: str = 'float') -> Tuple[any, ExifError]:
    '''
    Get a value with 'key' from 'tags'. This function does some validation and value transformation.

    Parameters
    ----------
    key : str
        Key to search for in the tags
    tags : Dict[str, any]
        Dict of EXIF tags
    is_numeric : bool
        Specifies if the value with 'key' is numeric. Default false

    Returns
    -------
    result : Tuple[any, ExifError]
        A result tuple consiting of the found value or an error
    '''
    if key not in tags.keys():
        return None, ExifError('Invalid key')

    value = tags.get(key)
    value = value.__str__()

    # If the user requested a numeric value (e.g. focal length or image width)
    if is_numeric:
        # If the value contains a '/' calculate the ratio
        if '/' in value:
            return utils.ratio_to_num(value, dtype), None

        # If the value contains no '/' just convert string to number
        if dtype == 'float':
            return float(value), None

        return int(value), None

    return value, None


def get_intrinsic_matrix(path: str) -> Tuple[np.ndarray, ExifError]:
    '''
    Calculates the intrinsic camera matrix based on EXIF data from a image located at 'path'.

    Parameters
    ----------
    path : str
        Path to the image

    Returns
    -------
    result : Tuple[np.ndarray, ExifError]
        The calculated matrix or an error
    '''
    tags, err = read(path)
    if err != None:
        return None, ExifError(f'Failed to read EXIF data in image {path}')

    focal_length, err = get('EXIF FocalLength', tags, True)
    if err != None:
        return None, ExifError('Failed to get focal length from EXIF tags')

    img_height, err = get('EXIF ExifImageLength', tags, True, 'int')
    if err != None:
        return None, ExifError('Failed to get image height from EXIF tags')

    img_width, err = get('EXIF ExifImageWidth', tags, True, 'int')
    if err != None:
        return None, ExifError('Failed to get image width from EXIF tags')

    # Magic numbers ahead, beware!
    # Sensor dimensions
    sensor_height = 4.29
    sensor_width = 5.76

    fx = img_width * focal_length / sensor_width
    fy = img_height * focal_length / sensor_height
    cx = img_width / 2.0
    cy = img_height / 2.0

    m = np.zeros((3, 3), np.float32)
    m[0, 0] = fx
    m[1, 1] = fy
    m[0, 2] = cx
    m[1, 2] = cy
    m[2, 2] = 0.0

    return m, None
