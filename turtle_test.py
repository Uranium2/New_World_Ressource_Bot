import json
import math
import time
import turtle
from typing import List, Union

import numpy as np

from my_player import My_player

screen = turtle.Screen()
screen.bgcolor("grey")
screen.title("Turtle")
skk = turtle.Turtle()

with open("route_1.json", "r") as fp:
    listObj = json.load(fp)

list_points = []

for key, value in listObj.items():
    value = (value[0], value[1])
    list_points.append(value)

maxs = list(map(max, zip(*list_points)))
mins = list(map(min, zip(*list_points)))

max_x = maxs[0]
max_y = maxs[1]

min_x = mins[0]
min_y = mins[1]


def minmax(x, min_, max_):
    return (x - min_) / (max_ - min_)


list_points_norm = []

for point in list_points:
    list_points_norm.append(
        (minmax(point[0], min_x, max_x), minmax(point[1], min_y, max_y))
    )

list_points = []
for value in list_points_norm:
    value = (value[0] * 100, value[1] * 100)
    list_points.append(value)

list_points = [np.array(l) for l in list_points]


def is_close_to_point(
    target: np.array, my_pos: np.array, epsilon_distance: float
) -> bool:
    """Check if player is next to target with an epsilon distance error

    Args:
        target (np.array): Target position
        my_pos (np.array): Player position
        epsilon_distance (float): minimum distance to return True

    Returns:
        bool: True, is close to target otherwise False
    """
    return distance(target, my_pos) <= epsilon_distance


def distance(target: np.array, my_pos: np.array) -> float:
    """Compute distance between 2 points

    Args:
        target (np.array): Target position
        my_pos (np.array): Player position

    Returns:
        float: Distance between targent and player
    """
    return math.sqrt(pow(target[0] - my_pos[0], 2) + pow(target[1] - my_pos[1], 2))


def get_index_closest_point(list_points: List[np.array], my_pos: np.array) -> int:
    """Get index of the closet point in a list of points

    Args:
        list_points (List[np.array]): List of points
        my_pos (np.array): Player position

    Returns:
        int: Index of the closet position in the list
    """
    closest_dist = distance(list_points[0], my_pos)
    index_in_list = 0

    for i, point in enumerate(list_points):
        dist = distance(point, my_pos)
        if dist < closest_dist:
            closest_dist = dist
            index_in_list = i

    return index_in_list


def pid(
    kp: float, ki: float, kd: float, dt: float, error: float, integral: float
) -> Union[float, float]:
    """PID controler

    Args:
        kp (float): proportional gain
        ki (float): integral gain
        kd (float): derivative gain
        dt (float): time derivative
        error (float): error at given time
        integral (float): integral. Init to 0 at start and assign at pid call

    Returns:
        Union[float, float]: Error value, integral
    """
    proportional_ = kp * error
    integral = integral + (ki * error * dt)
    derivative_ = -kd * error / dt
    return proportional_ + integral + derivative_, integral


def distance_from_line(point1: np.array, point2: np.array, my_pos: np.array) -> float:
    """Get shortest distance from line.

    Args:
        point1 (np.array): point1 of line
        point2 (np.array): point2 of line
        my_pos (np.array): point of player

    Returns:
        float: distance
    """
    return np.linalg.norm(np.cross(point2 - point1, point1 - my_pos)) / np.linalg.norm(
        point2 - point1
    )


def get_direction_from_errors(w: float) -> str:
    """Get direction to look at depending of error

    Args:
        w (float): error of system

    Returns:
        str: next key or direction to look at
    """
    if w < 1:
        return "left"
    if w > 1:
        return "right"
    return "nothing"


def is_point_above_line(point1: np.array, point2: np.array, my_pos: np.array) -> bool:
    """Check if the position of the player is above or under a line

    Args:
        point1 (np.array): point1 of line
        point2 (np.array): point2 of line
        my_pos (np.array): point of player

    Returns:
        bool: True player is above line. False player is under line
    """
    return np.cross(my_pos - point1, point2 - point1) < 0


def get_yaw(point1: np.array, point2: np.array) -> float:
    dx = point1[0] - point2[0]
    dy = point1[1] - point2[1]
    return math.atan2(dy, dx)


def get_pos(skk: turtle.Turtle) -> np.array:
    """Convert pos of turtle to np array of 2 coords

    Args:
        skk (turtle.Turtle): My turtle

    Returns:
        np.array: coordinates of the turtle in np.array
    """
    return np.array([skk.pos()[0], skk.pos()[1]])


skk.goto(0, 0)
my_player = My_player(*get_pos(skk))
print(my_player)


# init
skk.goto(0, 0)
my_pos = get_pos(skk)
index = 0  # get_index_closest_point(list_points, my_pos)
integral = 0.0
start_time = time.time()

ii = 0
while index < len(list_points):
    previous_target = list_points[index - 1]
    target = list_points[index]
    dist = distance(target, my_pos)
    while not is_close_to_point(target, my_pos, 1):
        dt = time.time() - start_time
        print(f"\nTrying to reach point {target} at index {index}")
        diff = target - my_pos
        dist = distance(target, my_pos)

        degree = my_player.get_target_orientation(target)
        diff_angle = my_player.diff_angle(degree)

        skk._rotate(diff_angle)
        print(f"Making {diff_angle=}")

        skk.forward(1)
        # time.sleep(1)

        # end loop, refresh pos and dist
        my_pos = get_pos(skk)
        dist = distance(target, my_pos)
        my_player.update(my_pos[0], my_pos[1])
        print(f"New pos {my_pos}. Dist from point {dist}")

    print(f"Reached point {target} at index {index}")
    index = index + 1

turtle.done()
