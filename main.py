from multiprocessing import Process

import PySimpleGUI as sg
from PIL import Image

from src.config import edit_config, load_config
from src.core import main_create_new_route, main_process
from src.utils import (
    RectangleSelection,
    make_window,
    set_process_state,
    take_screenshot,
)


def terminate_p(p):
    if p:
        p.terminate()


def main():
    run_key = "F9"
    config = load_config()
    window = make_window("New World - Ressource Bot", run_key)
    down_run_key = False
    p = None
    p_route = None


    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            terminate_p(p)
            terminate_p(p_route)
            break
        if event == "-POS-":
            terminate_p(p)
            terminate_p(p_route)
            down_run_key = set_process_state(False, window, run_key)
            img = Image.fromarray(take_screenshot(True))
            selector = RectangleSelection(img)
            while not selector.done:
                pass
            selector.close()
            edit_config("screenshot_rectangle", selector.rectangle, config)
        if event == run_key:
            down_run_key = set_process_state(not down_run_key, window, run_key)

        if event == "-RECORD_ROUTE-":
            print("test")
            route_name = values["-NEW_ROUTE_NAME-"]
            print(route_name)
            if route_name.isalnum():
                terminate_p(p)
                terminate_p(p_route)
                down_run_key = set_process_state(False, window, run_key)

                p_route = Process(
                    target=main_create_new_route,
                    args=(
                        config["screenshot_rectangle"],
                        route_name,
                    ),
                )
                p_route.start()
                print("started")

        if down_run_key:
            terminate_p(p)
            terminate_p(p_route)
            print("Starting process")
            p = Process(
                target=main_process,
                args=(config["screenshot_rectangle"],),
            )
            p.start()
        else:
            terminate_p(p)


if __name__ == "__main__":
    main()
