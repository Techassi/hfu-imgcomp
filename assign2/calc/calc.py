from typing import Any
import numpy as np
import utils.lines as lines
import cv2 as cv
import math


def do():
    pass


def main_van_v(vx: tuple, vy: tuple, b: tuple, b0: tuple) -> tuple:
    cross_line_bs = lines.get_line_from(b, b0)
    cross_line_vs = lines.get_line_from(vx, vy)
    v = lines.get_intersection_pos(cross_line_bs, cross_line_vs)

    return v


def calc_t(v: tuple, t0: tuple, r: tuple, b: tuple) -> tuple:
    cross_line_v_t = lines.get_line_from(v, t0)
    cross_line_r_b = lines.get_line_from(r, b)
    print(cross_line_r_b)
    t = lines.get_intersection_pos(cross_line_v_t, cross_line_r_b)

    return t


def calc_distance_points(point_a: tuple, point_b: tuple) -> float:
    sum = 0

    for i in range(len(point_a)):
        sum += (point_b[i] - point_a[i])**2

    return math.sqrt(sum)
