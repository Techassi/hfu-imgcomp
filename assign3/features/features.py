from typing import List, Tuple, TypeAlias
import cv2 as cv
import os

KeypointDescriptorList: TypeAlias = List[Tuple[List[cv.KeyPoint], List[List[float]]]]
FlannMatchesList: TypeAlias = List[Tuple[Tuple[cv.DMatch, cv.DMatch]]]
FilteredMatchesList: TypeAlias = List[Tuple[List, List]]


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
            print(i, j)
            # [ Tuple [ List [kpoints_in_i, kpoints_in_j], List [des_in_i, des_in_j] ] ]
            kpoints_in_i, des_in_i = sift.detectAndCompute(imgs[i], None)
            kpoints_in_j, des_in_j = sift.detectAndCompute(imgs[j], None)
            keypoints_descriptor_list.append(
                (
                    [kpoints_in_i, kpoints_in_j],
                    [des_in_i, des_in_j]
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
        matches.append(kp_matches)

    return matches


def filter_matches(kd_list: KeypointDescriptorList, fm_list: FlannMatchesList) -> FilteredMatchesList:
    ''''''
    # TODO (Techassi): Iterate over kd_list and the find the points in the matches list. Dont iterate over fm_list first
    filtered_matches: FilteredMatchesList = []
    for i, matches in enumerate(fm_list):
        points_in_left = []
        points_in_right = []

        for j, (m, n) in enumerate(matches):
            if m.distance < 0.8*n.distance:
                matchesMask = [[0, 0] for j in range(len(matches))]
                matchesMask[i] = [1, 0]

                # points_in_left.append(kd_list[i][0])
                print(len(kd_list[i][0]), m.queryIdx)
                # print(kd_list[i][0][m.queryIdx].pt)

                # filtered_matches[i]

                # pts1.append(kp1[m.queryIdx].pt)
                # pts2.append(kp2[m.trainIdx].pt)
