import cv2 as cv


def circle(img, pos: tuple, color: tuple = (0, 0, 0), radius: int = 5, thickness: int = 10, window_name: str = 'win'):
    '''
    Draw circle in 'img' at 'x' and 'y' with 'color'.

    Parameters
    ----------
    img : Mat
        Image matrix
    pos : tuple
        X and Y position
    color : tuple
        Color of the circle (Default 0, 0, 0)
    '''
    cv.circle(img, pos, radius, color, thickness)
    cv.imshow(window_name, img)


def line(img, a: tuple, b: tuple, color: tuple = (244, 164, 96), thickness: int = 5, type: int = cv.LINE_AA, window_name: str = 'win'):
    '''
    Draw a line between two points 'a' and 'b' with 'color'.

    Parameters
    ----------
    img : Mat
        Image matrix
    a : tuple
        First point
    b : tuple
        Second point
    color : tuple
        Color of the line (Default 244, 164, 96)
    '''
    cv.line(img, a, b, color, 5)
    cv.imshow(window_name, img)


def vline_world(world_img: any, world_van_horiz: tuple, world_van_vert: tuple, window_name: str = 'win') -> None:
    ''''''
    circle(world_img, world_van_horiz, (255, 0, 255), 20, -1, window_name)
    circle(world_img, world_van_vert, (0, 0, 255), 10, -1, window_name)
    line(world_img, world_van_horiz, world_van_vert, (0, 0, 255), 3, cv.LINE_AA, window_name)


def render_image(img: any, render_data: dict, window_name: str = 'win'):
    '''
    Render an image with the provided render data.

    Parameters
    ----------
    img : Mat
        The base image
    render_data : dict
        Render data containing various points
    window_name : str
        Display window name (Default: win)
    '''
    # Draw points and lines of first pair of lines
    for i, p in enumerate(render_data['f_list']):
        cv.circle(img, p, 5, (0, 0, 255), 10)
        if i % 2 != 0:
            cv.line(img, render_data['f_list'][i-1], p, (244, 164, 96), 3)

    # Draw points and lines of second pair of lines
    for i, p in enumerate(render_data['s_list']):
        cv.circle(img, p, 5, (0, 255, 0), 10)
        if i % 2 != 0:
            cv.line(img, render_data['s_list'][i-1], p, (244, 164, 96), 3)

    # Draw points and line of bottle height
    for i, p in enumerate(render_data['b_list']):
        cv.circle(img, p, 5, (91, 113, 255), 10)
        if i % 2 != 0:
            cv.line(img, render_data['b_list'][i-1], p, (244, 164, 96), 3)

    # Draw points and line of mug height
    for i, p in enumerate(render_data['m_list']):
        cv.circle(img, p, 5, (91, 113, 255), 10)
        if i % 2 != 0:
            cv.line(img, render_data['m_list'][i-1], p, (244, 164, 96), 3)

    cv.imshow(window_name, img)
