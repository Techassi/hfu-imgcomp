from typing import List, Tuple
import numpy as np
import cv2 as cv
import os

from .types import EpilinesList, FilteredMatchesList, FlannMatchesList, FundamentalMatricesList, KeypointDescriptorList


class FeaturesError:
    def __init__(self, message: str) -> None:
        self.message = message


def load_images(paths: List[str]) -> Tuple[List[cv.Mat], FeaturesError]:
    '''
    Load n images from 'paths' via OpenCV at the same time in grayscale.

    Parameters
    ----------
    paths : List[str]
        List of image paths

    Returns
    -------
    result : Tuple[List[any], FeaturesError]
        List of images (matrices) or an error
    '''
    images = []

    for path in paths:
        if not os.path.exists(path):
            return images, FeaturesError(f'Image at {path} does not exist')

        try:
            img = cv.imread(path, cv.IMREAD_GRAYSCALE)
            # img = cv.resize(img, (0, 0), fx=0.5, fy=0.5)
            images.append(img)
        except:
            return images, FeaturesError(f'Failed to read image at {path}')

    return images, None


def get_combinations(imgs: List[cv.Mat]) -> List[List[int]]:
    '''
    Return all possible image combinations.

    Parameters
    ----------
    imgs : List[cv.Mat]
        List of images

    Returns
    -------
    combis : List[List[int]]
        A list of a list of combinations
    '''
    combinations: List[List[int]] = []

    for i, _ in enumerate(imgs):
        if i == len(imgs) - 1:
            break

        combinations.append([])
        for j in range(1, len(imgs) - i):
            combinations[i].append(i + j)

    return combinations


def get_keypoints(imgs: List[cv.Mat]) -> KeypointDescriptorList:
    '''
    Return a list of keypoints and descriptors for each combination.

    Parameters
    ----------
    imgs : List[cv.Mat]
        List of images

    Returns
    -------
    list : KeypointDescriptorList
        A list of keypoints and descriptors for each combination
    '''
    # Get possible image combinations
    combis = get_combinations(imgs)

    # Create SIFT object
    sift = cv.SIFT_create(nfeatures=500)

    # Iterate over all combinations
    keypoints_descriptor_list: KeypointDescriptorList = []
    for i, c in enumerate(combis):
        for j in c:
            # [ Tuple [ List [ List[kpoints_in_i], List[kpoints_in_j] ], List [des_in_i, des_in_j] ] ]
            kpoints_in_i, des_in_i = sift.detectAndCompute(imgs[i], None)
            kpoints_in_j, des_in_j = sift.detectAndCompute(imgs[j], None)

            keypoints_descriptor_list.append(
                (
                    [list(kpoints_in_i), list(kpoints_in_j)],
                    [des_in_i, des_in_j],
                    (i, j)
                )
            )

    return keypoints_descriptor_list


def match_keypoints(kd_list: KeypointDescriptorList, trees: int = 5, checks: int = 5, k: int = 2) -> FlannMatchesList:
    ''''''
    # TODO (Techassi): Ask about the number of matches. Should they really be that HIGH? /shrug
    # Setup flann matcher params
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=trees)
    search_params = dict(checks=checks)

    # Create flann matcher
    flann_Matcher = cv.FlannBasedMatcher(index_params, search_params)

    # Iterate ober all combinations and calculate matches
    matches: FlannMatchesList = []
    for combi in kd_list:
        kp_matches = flann_Matcher.knnMatch(combi[1][0], combi[1][1], k=k)
        matches.append((kp_matches, combi[2]))

    return matches


def filter_matches(kd_list: KeypointDescriptorList, fm_list: FlannMatchesList) -> FilteredMatchesList:
    '''
    Filter matches based on distance to each other.

    Parameters
    ----------
    kd_list : KeypointDescriptorList
        A list of keypoints and descriptors for each combination
    fm_list : 
        A list of matched keypoints for each combination

    Returns
    -------
    filtered_matches : FilteredMatchesList
        A list of filtered matches for each combination
    '''
    filtered_matches: FilteredMatchesList = []

    for i, kd in enumerate(kd_list):
        matchesMask = [[0, 0] for k in range(len(fm_list[i][0]))]
        points_in_right = []
        points_in_left = []

        for j, (m, n) in enumerate(fm_list[i][0]):
            if m.distance < 0.8*n.distance:
                matchesMask[j] = [1, 0]

                points_in_right.append(kd[0][1][m.trainIdx].pt)
                points_in_left.append(kd[0][0][m.queryIdx].pt)

        filtered_matches.append(
            (
                np.int32(points_in_left),
                np.int32(points_in_right),
                matchesMask,
                fm_list[i][1]
            )
        )

    return filtered_matches


def get_fundamental_matrices(fm_list: FilteredMatchesList) -> FundamentalMatricesList:
    '''
    Find fundamental matrix for each combination.

    Parameters
    ----------
    fm_list : FilteredMatchesList
        A list of filtered matches for each combination

    Returns
    -------
    list : FundamentalMatricesList
        A list of the fundamental matrix, the mask, and inlier points (left and right) for each combination
    '''
    m_list: FundamentalMatricesList = []

    for m in fm_list:
        f, mask = cv.findFundamentalMat(m[0], m[1], cv.FM_RANSAC)
        points_in_right = m[1][mask.ravel() == 1]
        points_in_left = m[0][mask.ravel() == 1]

        m_list.append((f, mask, points_in_left, points_in_right, m[3]))

    return m_list


def compute_epilines(fm_list: FundamentalMatricesList) -> EpilinesList:
    '''
    Compute the epilines for the left and right image of all combinations.

    Parameters
    ----------
    fm_list : FundamentalMatricesList
        A list of the fundamental matrix, the mask, and inlier points (left and right)

    Returns
    -------
    epilines_list : EpilinesList
        A list of epilines (left and right) for each combination
    '''
    epilines_list: EpilinesList = []
    for item in fm_list:
        right_lines = cv.computeCorrespondEpilines(item[3].reshape(-1, 1, 2), 2, item[0])
        right_lines = right_lines.reshape(-1, 3)

        left_lines = cv.computeCorrespondEpilines(item[2].reshape(-1, 1, 2), 1, item[0])
        left_lines = left_lines.reshape(-1, 3)

        epilines_list.append(
            (
                (left_lines, right_lines),
                item[4]
            )
        )

    return epilines_list


def get_epilines(imgs: List[cv.Mat]) -> EpilinesList:
    ''''''
    kp_list = get_keypoints(imgs)
    mk_list = match_keypoints(kp_list)
    fm_list = filter_matches(kp_list, mk_list)
    m_list = get_fundamental_matrices(fm_list)
    return compute_epilines(m_list)
