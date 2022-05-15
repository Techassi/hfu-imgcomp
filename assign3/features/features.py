import numpy as np
import cv2 as cv

from thints.images import ImageList
from thints.features import (
    FundamentalMatricesList,
    KeypointDescriptorList,
    FilteredMatchesList,
    FlannMatchesList,
    CombinationsList,
    EpilinesList,
    PointsList
)


class FeaturesError:
    def __init__(self, message: str) -> None:
        self.message = message


def get_combinations(imgs: ImageList) -> CombinationsList:
    '''
    Return all possible image combinations.

    Parameters
    ----------
    imgs : ImageList
        List of images

    Returns
    -------
    combis : CombinationsList
        A list of a list of combinations
    '''
    combinations: CombinationsList = []

    for i, _ in enumerate(imgs):
        if i == len(imgs) - 1:
            break

        combinations.append([])
        for j in range(1, len(imgs) - i):
            combinations[i].append(i + j)

    return combinations


def get_keypoints(imgs: ImageList) -> KeypointDescriptorList:
    '''
    Return a list of keypoints and descriptors for each combination.

    Parameters
    ----------
    imgs : ImageList
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


def find_fundamental_matrices(fm_list: FilteredMatchesList) -> FundamentalMatricesList:
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


def get_epilines(imgs: ImageList) -> EpilinesList:
    '''
    Calculate epilines from a set of images.

    Parameters
    ----------
    imgs : ImageList
        List of image matrices

    Returns
    -------
    epilines : EpilinesList
         A list of epilines for each combination of images
    '''
    kp_list = get_keypoints(imgs)
    mk_list = match_keypoints(kp_list)
    fm_list = filter_matches(kp_list, mk_list)
    fm_list = find_fundamental_matrices(fm_list)
    return compute_epilines(fm_list)


def get_points(imgs: ImageList) -> PointsList:
    '''
    Find matching points in a set of two images for every combination.

    Parameters
    ----------
    imgs : ImageList
        List of image matrices

    Returns
    -------
    epilines : PointsList
         A list of matching points for each combination of images
    '''
    points_list = []

    kp_list = get_keypoints(imgs)
    mk_list = match_keypoints(kp_list)
    fm_list = filter_matches(kp_list, mk_list)

    for i, k in enumerate(kp_list):
        points_list.append(
            (
                k[0][0],
                k[0][1],
                mk_list[i][0],
                fm_list[i][2],
                k[2]
            )
        )

    return points_list


def get_fundamental_matrices(imgs: ImageList) -> FundamentalMatricesList:
    ''''''
    kp_list = get_keypoints(imgs)
    mk_list = match_keypoints(kp_list)
    fm_list = filter_matches(kp_list, mk_list)
    fm_list = find_fundamental_matrices(fm_list)
    return fm_list
