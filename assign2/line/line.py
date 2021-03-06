from typing import Any, Literal
from enum import Enum
import numpy as np
import cv2 as cv
import operator
import click

import utils.wait_reset as wait_reset
import utils.geometry as geometry
import utils.drawing as drawing
import utils.images as images
import utils.input as inp
import calc.calc as calc


clicked_object_points = []
world_img_copy = None
vanishing_points = []
clicked_points = []


def handle_click(img: any, event: any, x: int, y: int, flags: any, param: any):
    '''
    Handle left mouse button click.

    Parameters
    ----------
    img : Mat
        Image
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

    if len(clicked_object_points) % 2 == 0 and len(clicked_object_points) != 0:
        drawing.line(img, clicked_object_points[-1], clicked_object_points[-2])

    if len(clicked_points) == 4 and len(vanishing_points) < 2:
        first_line = geometry.line_from(clicked_points[0], clicked_points[1])
        second_line = geometry.line_from(clicked_points[2], clicked_points[3])
        vanishing_point = geometry.intersection_from(first_line, second_line)
        drawing.circle(img, vanishing_point, (0, 0, 255))
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
        click.echo(str(erg * pixel_ratio) + ' cm')


def store_vanishing_points(vanishing_point: tuple):
    global vanishing_points

    click.echo(f"Calculated intersection/vanishing point at: {vanishing_point}")
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

    click.echo(
        f"World coords: min_x: {min_world_x}, max_x: {max_world_x}, min_y: {min_world_y}, max_y: {max_world_y}")

    # Pixel border so that vanishing points are fully visible
    # Otherwise they may be directly on img edges
    border = 50

    world_width = max_world_x - min_world_x + (border * 2)
    world_height = max_world_y - min_world_y + (border * 2)

    click.echo(f"World size: ({world_width}, {world_height})")

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

    click.echo(f"Origin: {origin}")
    click.echo(f"Width/Height: {img_width} / {img_height}")
    click.echo(img.shape)
    click.echo(
        f"Adjusted vanishing points: {adjusted_van_point_horiz}, {adjusted_van_point_vert}")

    world_img[origin[1]:origin[1]+img_height, origin[0]:origin[0]+img_width, :] = img
    world_img_copy = world_img

    drawing.vline_world(world_img, adjusted_van_point_horiz, adjusted_van_point_vert)


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

    def callback(event, x, y, flags, param): handle_click(img, event, x, y, flags, param)

    cv.setMouseCallback(window_name, callback)

    wait_reset.wait_reset(10, clicked_points, img_copy, window_name)
