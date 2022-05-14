import math


def ratio_to_num(ratio: str, dtype: str) -> float | int:
    '''
    Calculates the numeric value of a string formed 'n/d'. Returns 0 if failed.

    Parameters
    ----------
    ratio : str
        The ratio string

    Returns
    -------
    num : float
        Returns the numeric value of the ratio. 0 if failed
    '''
    parts = ratio.split('/')
    if len(parts) == 1:
        try:
            if dtype == 'float':
                return float(parts[0])

            return int(parts[0])
        except:
            return 0

    if len(parts) != 2:
        return 0

    try:
        numerator = float(parts[0])
        denominator = float(parts[1])

        if dtype == 'float':
            return numerator / denominator

        return math.floor(numerator / denominator)
    except:
        return 0
