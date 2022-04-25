from typing import Any, Literal
import cv2 as cv
import click
import numpy as np
import operator
import copy

import utils.images as images
import utils.lines as lines
import utils.input as inp
import utils.wait_reset as wait_reset
import calc.calc as calc

clicked_points = []
clicked_object_points = []
vanishing_points = []
world_img_copy = None


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
    global vanishing_points, clicked_points, clicked_object_points

    # Ignore everything except left mouse button clicks
    if event != cv.EVENT_LBUTTONDOWN:
        return

    # If we have enough points to calculate and draw vanishing line
    if len(clicked_points) >= 8:
        return

    # Append point to list and draw point in image
    clicked_points.append((x, y))
    draw_circle(img, x, y)

    # If we have an even number of points, draw line
    if len(clicked_points) % 2 == 0 and len(clicked_points) != 0:
        draw_line(img, clicked_points[-1], clicked_points[-2])

    if len(clicked_object_points) % 2 == 0 and len(clicked_object_points) != 0:
        draw_line(img, clicked_object_points[-1], clicked_object_points[-2])

    if len(clicked_points) == 4 and len(vanishing_points) < 2:
        first_line = lines.get_line_from(clicked_points[0], clicked_points[1])
        second_line = lines.get_line_from(clicked_points[2], clicked_points[3])
        vanishing_point = lines.get_intersection_pos(first_line, second_line)
        draw_circle(img, vanishing_point[0], vanishing_point[1], (0, 0, 255))
        store_vanishing_points(vanishing_point)

    if len(vanishing_points) == 2 and len(clicked_points) == 8:
        clicked_object_points = clicked_points[4:]

    if len(vanishing_points) == 2 and len(clicked_object_points) == 4:
        world_img, min_world_x, min_world_y, border = create_world_image(x, img)
        translate_world_img(img, world_img, min_world_x, min_world_y, border)
        get_v()
        get_t()
        cr = cross_ratio(calc_H(), calc_R())
        erg = calc_H() / cr
        # Magic number hey
        pixel_ratio = 0.0264583333
        print(str(erg * pixel_ratio) + ' cm')


def store_vanishing_points(vanishing_point: tuple):
    global vanishing_points

    print(f"Calculated intersection/vanishing point at: {vanishing_point}")

    van_length = len(vanishing_points)

    if(van_length == 0):
        vanishing_points = [vanishing_point]
    else:
        vanishing_points.append(vanishing_point)


# Create world image huge enough, so that vanishing points are visible
def create_world_image(x: Any, img: Any) -> Any:
    img_height, img_width, _ = img.shape
    # Returns either 0 or first vanishing point in list, whichever is lower
    min_world_x = min(min(vanishing_points)[0], 0)
    # If vanishing point coords are > than original img width,
    # vanishing point = new img width. If not, keep orig img width
    max_world_x = max(max(vanishing_points)[0], img_width)
    min_world_y = min(min(vanishing_points, key=lambda x: x[1])[1], 0)
    max_world_y = max(max(vanishing_points, key=lambda x: x[1])[1], img_height)

    print(
        f"World coords: min_x: {min_world_x}, max_x: {max_world_x}, min_y: {min_world_y}, max_y: {max_world_y}")

    # Pixel border so that vanishing points are fully visible
    # Otherwise they may be directly on img edges
    border = 50

    world_width = max_world_x - min_world_x + (border * 2)
    world_height = max_world_y - min_world_y + (border * 2)

    print(f"World size: ({world_width}, {world_height})")

    # 3D world image of calculated width & height

    world_img = np.zeros((world_height, world_width, 3), np.uint8)

    return world_img, min_world_x, min_world_y, border


def translate_world_img(img: Any,
                        world_img: Any,
                        min_world_x: int,
                        min_world_y: int,
                        border: Literal[50]) -> None:

    global world_img_copy

    img_height, img_width, _ = img.shape
    origin = (abs(min_world_x) + border, abs(min_world_y) + border)
    adjusted_van_point_horiz = tuple(map(operator.add, vanishing_points[0], origin))
    adjusted_van_point_vert = tuple(map(operator.add, vanishing_points[1], origin))

    print(f"Origin: {origin}")
    print(f"Width/Height: {img_width} / {img_height}")
    print(img.shape)
    print(
        f"Adjusted vanishing points: {adjusted_van_point_horiz}, {adjusted_van_point_vert}")

    world_img[origin[1]:origin[1]+img_height, origin[0]:origin[0]+img_width, :] = img
    world_img_copy = world_img

    draw_vans_in_world(world_img, adjusted_van_point_horiz, adjusted_van_point_vert, 'win')


def draw_vans_in_world(world_img: Any,
                       world_van_horiz: tuple,
                       world_van_vert: tuple,
                       title: str) -> None:

    cv.circle(world_img, world_van_horiz, 20, (255, 0, 255), -1)
    cv.circle(world_img, world_van_vert, 10, (0, 0, 255), -1)
    cv.line(world_img,
            world_van_horiz,
            world_van_vert,
            (0, 0, 255),
            3,
            cv.LINE_AA)
    cv.imshow(title, world_img)


def get_v() -> tuple:
    global vanishing_points, clicked_object_points, world_img_copy
    v = calc.main_van_v(vanishing_points[0],
                        vanishing_points[1],
                        clicked_object_points[1],
                        clicked_object_points[3])

    return v


def get_t() -> tuple:
    global vanishing_points, clicked_object_points, world_img_copy

    t = calc.calc_t(get_v(),
                    clicked_object_points[0],
                    clicked_object_points[2],
                    clicked_object_points[3])

    return t


def calc_R() -> float:
    R = calc.calc_distance_points(clicked_object_points[2],
                                  clicked_object_points[3])

    return R


def calc_H() -> float:
    H = calc.calc_distance_points(get_t(), clicked_object_points[3])

    return H


def cross_ratio(H: float, R: float) -> float:
    return H / R


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
    img_copy = img.copy()
    cv.namedWindow(window_name, cv.WINDOW_GUI_NORMAL)
    cv.imshow(window_name, img)

    def callback(event, x, y, flags, param): return handle_click(img, event, x, y, flags, param)
    cv.setMouseCallback(window_name, callback)

    wait_reset.wait_reset(10, clicked_points, img_copy, window_name)


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
