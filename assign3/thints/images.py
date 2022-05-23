from typing import List, Tuple, TypeAlias
import cv2 as cv


ImageList: TypeAlias = List[Tuple[cv.Mat, str]]
CombinationsList: TypeAlias = List[List[int]]
