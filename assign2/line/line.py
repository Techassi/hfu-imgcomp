import cv2 as cv
import click

import utils.images as images
import utils.lines as lines
import utils.input as inp
import utils.wait as wait

clicked_points = []


def handle_click(img, event, x, y, flags, param):
    '''
    Handle left mouse button click.

    Parameters
    ----------
    img : Mat
        Image
    event : int
        OpenCV event code
    x : Any
        X component of the clicked position
    y : Any
        Y component of the clicked position
    flags : Any
    param : Any
    '''
    global vanishing_points, clicked_points

    # Ignore everything except left mouse button clicks
    if event != cv.EVENT_LBUTTONDOWN:
        return

    # If we have enough points to calculate and draw vanishing line
    if len(clicked_points) >= 4:
        return

    # Append point to list and draw point in image
    clicked_points.append((x, y))
    draw_circle(img, x, y)

    # If we have an even number of points, draw line
    if len(clicked_points) % 2 == 0 and len(clicked_points) != 0:
        draw_line(img, clicked_points[-1], clicked_points[-2])

    if len(clicked_points) == 4:
        first_line = lines.get_line_from(clicked_points[0], clicked_points[1])
        second_line = lines.get_line_from(clicked_points[2], clicked_points[3])
        vanishing_point = lines.get_intersection_pos(first_line, second_line)
        draw_circle(img, vanishing_point[0], vanishing_point[1], (0, 0, 255))


def do(base_path: str):
    '''
    Compute the vanishing line based on a selected plane.

    Parameters
    ----------
    base_path : str
        Base path of source image files
    '''
    window_name = 'win'

    # Glob images
    img_paths, ok = images.list(base_path)
    if not ok:
        return

    # Display found images
    click.echo(f'Found <{len(img_paths)}> image(s)')
    images.print_list(img_paths)

    index = inp.enforce_range_input(
        f'Enter number between 1 and {len(img_paths)} to select image to use: ', 1, len(img_paths))

    img = cv.imread(img_paths[index-1])
    cv.imshow(window_name, img)

    def callback(event, x, y, flags, param): return handle_click(img, event, x, y, flags, param)
    cv.setMouseCallback(window_name, callback)

    wait.wait(10)


def draw_circle(img, x: int, y: int, color: tuple = (0, 0, 0)):
    '''
    Draw circle in 'img' at 'x' and 'y' with 'color'.

    Parameters
    ----------
    img : Mat
        Image matrix
    x : int
        X position
    y : int
        Y position
    color : tuple
        Color of the circle (Default 0, 0, 0)
    '''
    cv.circle(img, (x, y), 5, color, 10)
    cv.imshow('win', img)


def draw_line(img, a: tuple, b: tuple, color: tuple = (244, 164, 96)):
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
    cv.imshow('win', img)
