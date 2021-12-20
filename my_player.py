import math

import numpy as np


class My_player:
    """Representation of player in the game"""

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.last_x = x
        self.last_y = y
        self.rotate = 0
        self.direction = self.get_self_orientation()

    def update(self, x: float, y: float) -> None:
        """Update position of player, last position and direction

        Args:
            x (float): new X position
            y (float): new Y position
        """
        self.last_x = self.x
        self.last_y = self.y
        self.x = x
        self.y = y
        self.direction = self.get_self_orientation()

    def get_position(self) -> np.array:
        """Return position of player

        Returns:
            np.array: [x, y] position of player
        """
        return np.array([self.x, self.y])

    def get_last_position(self) -> np.array:
        """Return last position of player

        Returns:
            np.array: [x, y] last position of player
        """
        return np.array([self.last_x, self.last_y])

    def diff_angle(self, new_angle: float) -> float:
        """Compare the orientation of the player to a given angle (mostly target orientation from world's perspective)

        Args:
            new_angle (float): new angle to compare

        Returns:
            float: angle
        """
        angle = new_angle - self.get_self_orientation()
        self.rotate = angle
        return angle

    def get_self_orientation(self) -> float:
        """Get angle from the vector player and player_last_position

        Returns:
            float: angle
        """
        x, y = self.get_position() - self.get_last_position()
        return round(math.degrees(math.atan2(y, x)), 10) % 360.0

    def get_target_orientation(self, target: np.array) -> float:
        """Get angle from the vector player-target and the world

        Returns:
            float: angle
        """
        x, y = target - self.get_position()
        return round(math.degrees(math.atan2(y, x)), 10) % 360.0

    def __str__(self) -> str:
        """Print attributes of class for debugging

        Returns:
            str: string printed when call `print()` on class object
        """
        string = ""
        for key, value in self.__dict__.items():
            string = string + f"{key}={value}\n"
        return string
