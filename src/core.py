from time import sleep

import keyboard
from PIL import ImageGrab

from .create_route import get_pos, log_pos_to_file


def main_create_new_route(rectangle, file_name):
    i = 0
    while True:
        if keyboard.read_key() == "n":
            x = rectangle[0]
            y = rectangle[1]
            x_2 = rectangle[2] + x
            y_2 = rectangle[3] + y
            bbox = (x, y, x_2, y_2)
            img = ImageGrab.grab(bbox=bbox)
            pos = get_pos(img)
            if pos:
                log_pos_to_file(f"routes/{file_name}.json", i, pos[0])
                i = i + 1


def main_process(rectangle):
    while True:
        print("Hello world")
        sleep(1)