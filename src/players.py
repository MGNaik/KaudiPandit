from enum import Enum
from src.types import Position


class PlayerID(Enum):
    Bottom = 0
    Right = 1
    Top = 2
    Left = 3

class Player:
    def __init__(self, id):
        self.id = id
        self.starting_square = Position(6,3) # TODO: Derive from rotation
        


    
        