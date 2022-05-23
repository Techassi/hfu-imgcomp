from typing import List, Tuple, TypeAlias
import numpy as np
import cv2 as cv

KeypointDescriptorList: TypeAlias = List[
    Tuple[
        List[List[cv.KeyPoint]],
        List[List[float]],
        Tuple[int, int]
    ]
]

FlannMatchesList: TypeAlias = List[
    Tuple[
        Tuple[Tuple[cv.DMatch, cv.DMatch]],
        Tuple[int, int]
    ]
]

FundamentalMatricesList: TypeAlias = List[
    Tuple[
        np.ndarray,
        np.ndarray,
        List,
        List,
        Tuple[int, int]
    ]
]

FilteredMatchesList: TypeAlias = List[
    Tuple[
        List,
        List,
        List[List[int]],
        Tuple[int, int]
    ]
]

EpilinesList: TypeAlias = List[
    Tuple[
        Tuple[np.ndarray, np.ndarray],
        Tuple[int, int]
    ]
]

PointsList: TypeAlias = List[
    Tuple[
        List[cv.KeyPoint],
        List[cv.KeyPoint],
        Tuple[Tuple[cv.DMatch, cv.DMatch]],
        List[List[int]],
        Tuple[int, int]
    ]
]

EssentialMatricesList: TypeAlias = List[
    Tuple[
        np.ndarray,
        np.ndarray,
        np.ndarray,
        np.ndarray,
        Tuple[int, int]
    ]
]
