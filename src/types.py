from typing import NamedTuple

class Position(NamedTuple):
    row: int
    col: int

class Square(NamedTuple):
    position: Position
    safe: bool
    is_final: bool

def rotate_ccw(pos, n=7):
    r, c = pos
    return Position(n - 1 - c, r)

def rotate_ccw_path(path):
    newpath = {}
    for key in path:
        newpath.update({rotate_ccw(key):[rotate_ccw(val) for val in path[key]]})
    return newpath
