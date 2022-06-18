import click

from typing import Tuple


def range_input(message: str, min: int, max: int, verbose: bool = True) -> Tuple[int, bool]:
    '''
    Retrieve an integer input between 'min' and 'max' from the user.

    Parameters
    ----------
    message : str
        Message to display for the input prompt
    min : int
        Minimum value of range
    max : int
        Maximum value of range
    verbose : bool
        If status messages should be printed (Default: True)

    Returns
    -------
    value : int
        The input value or -1 when invalid
    ok : bool
        The status of this function
    '''
    input_value = input(message)

    # Convert to integer
    index = -1
    try:
        index = int(input_value)
    except:
        if verbose:
            click.echo('Invalid input. Exiting')
        return (index, False)

    # Check if in range
    if index < min or index > max:
        if verbose:
            click.echo('Invalid index. Out of range. Exiting')
        return (index, False)

    return (index, True)


def enforce_range_input(message: str, min: int, max: int) -> int:
    '''
    Retrieve an integer input between 'min' and 'max' from the user.
    If the user provides an invalid input, try again.

    Parameters
    ----------
    message : str
        Message to display for the input prompt
    min : int
        Minimum value of range
    max : int
        Maximum value of range

    Returns
    -------
    value : int
        The valid input value
    '''
    v, ok = range_input(message, min, max, False)
    while not ok:
        click.echo('Invalid input. Try again')
        v, ok = range_input(message, min, max, False)

    return v
