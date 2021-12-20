import json
import os
import re
from typing import List

import cv2
import numpy as np
import pytesseract


def unsharp_mask(
    image: np.array,
    kernel_size: List[int, int] = (5, 5),
    sigma: float = 1.0,
    amount: float = 1.0,
) -> np.array:
    """Apply unsharp mask to image. To make "pop" out text from background.

    Args:
        image (np.array): image
        kernel_size (List[int, int], optional): size to apply filter. Defaults to (5, 5).
        sigma (float, optional): Blurring coefficient. Defaults to 1.0.
        amount (float, optional): Sharpen coefficient. Defaults to 1.0.

    Returns:
        np.array: unsharpened image
    """
    image = np.array(image)
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    return sharpened


def get_pos(img_crop: np.aray) -> List[int, int]:
    """Uses tesseract to get position of player in the cropped image.

    Args:
        img_crop (np.aray): cropped image

    Raises:
        InterruptedError: Not a raise, just to check if `playerLocation_re` has all the data. Else, did not get clean data and returns None.

    Returns:
        List[int, int]: Coordinate X and Y of the player from the image
    """
    pytesseract.pytesseract.tesseract_cmd = (
        "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    )
    img_crop_filter = cv2.inRange(
        np.array(img_crop), np.array([100, 100, 100]), np.array([255, 255, 255])
    )
    img_crop_filter_unsharp = unsharp_mask(img_crop_filter)
    playerLocation = pytesseract.image_to_string(
        img_crop_filter_unsharp, config="-c tessedit_char_whitelist=[].,0123456789"
    )
    playerLocation_re = re.findall(
        r"\[(\d{1,5})[,.]{1,2}\d{1,3}[,.]{1,2}(\d{1,5})[,.]", playerLocation
    )
    try:
        if (
            int(playerLocation_re[0][0]) < 4300
            or int(playerLocation_re[0][0]) > 14200
            or int(playerLocation_re[0][1]) < -100
            or int(playerLocation_re[0][1]) > 10000
        ):
            raise InterruptedError("INTERCEPTED OUT OF MAP JUMP")
        return playerLocation_re
    except Exception as e:
        print(f"Could not decode position of player in {playerLocation=}")
        return None


def log_pos_to_file(path: str, i: int, pos: List[int, int]) -> None:
    """Log positions to a json file. Be careful, this function WILL overwritte existing files

    Args:
        path (str): path of file
        i (int): node index of position
        pos (List[int, int]): tuple (x, y) of position of the player
    """

    print(f"Adding element {pos} at node {i}")
    if not os.path.isfile(path):
        with open(path, "w+") as outfile:
            json.dump(
                {},
                outfile,
                indent=4,
            )

    with open(path) as fp:
        listObj = json.load(fp)

    listObj[i] = (int(pos[0]), int(pos[1]))

    with open(path, "w+") as outfile:
        json.dump(
            listObj,
            outfile,
            indent=4,
        )
