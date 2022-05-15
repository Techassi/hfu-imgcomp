from typing import List, Tuple, TypeAlias, TypedDict
import numpy as np


RectificationMatricesList: TypeAlias = List[
    Tuple[
        np.ndarray,
        np.ndarray,
        Tuple[int, int],
        Tuple[int, int],
        Tuple[int, int]
    ]
]

DepthMapsList: TypeAlias = List[Tuple[np.ndarray, Tuple[int, int]]]


class BMParams(TypedDict):
    numDisparities: int
    blockSize: int


class SGBMParams(TypedDict):
    speckleWindowSize: int
    uniquenessRatio: int
    numDisparities: int
    disp12MaxDiff: int
    minDisparity: int
    speckleRange: int
    blockSize: int
