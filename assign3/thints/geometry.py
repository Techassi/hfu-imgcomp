from typing import List, Tuple, TypeAlias
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
