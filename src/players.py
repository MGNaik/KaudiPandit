from enum import Enum
from src.types import Position, rotate_ccw
from src.pieces import Piece



class PlayerID(Enum):
    Bottom = 0
    Right = 1
    Top = 2
    Left = 3


class Player:
    def __init__(self, id):
        self.id = id
        
        square = Position(6, 3)
        for _ in range(self.id.value):
            square = rotate_ccw(square)
        self.starting_square = square

        self.pieces = []
        for i in range(6):
            self.pieces.append(Piece(self,i))
        self.piece_tuples = []



                
        



    
        