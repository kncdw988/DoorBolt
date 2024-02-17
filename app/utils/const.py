from enum import Enum


class Position(Enum):
    """ Position enumeration """
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3
    CENTER = 4
    TOP_LEFT = 5
    TOP_RIGHT = 6
    BOTTOM_LEFT = 7
    BOTTOM_RIGHT = 8