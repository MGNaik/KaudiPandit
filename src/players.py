from enum import Enum
from docs.Rules.src.types import Position, rotate_ccw, rotate_ccw_path
from docs.Rules.src.pieces import Piece


BOTTOM_PATH = {
    Position(6,3): [Position(6,4)],
    Position(6,4): [Position(6,5)],
    Position(6,5): [Position(6,6)],
    Position(6,6): [Position(5,6)],
    Position(5,6): [Position(4,6)],
    Position(4,6): [Position(3,6)],
    Position(3,6): [Position(2,6)],
    Position(2,6): [Position(1,6)],
    Position(1,6): [Position(0,6)],
    Position(0,6): [Position(0,5)],
    Position(0,5): [Position(0,4)],
    Position(0,4): [Position(0,3)],
    Position(0,3): [Position(0,2)],
    Position(0,2): [Position(0,1)],
    Position(0,1): [Position(0,0)],
    Position(0,0): [Position(1,0)],
    Position(1,0): [Position(2,0)],
    Position(2,0): [Position(3,0)],
    Position(3,0): [Position(4,0)],
    Position(4,0): [Position(5,0)],
    Position(5,0): [Position(6,0)],
    Position(6,0): [Position(6,1)],
    Position(6,1): [Position(6,2)],
    Position(6,2): [Position(5,1), Position(6,3)],
    Position(5,1): [Position(4,1)],
    Position(4,1): [Position(3,1)],
    Position(3,1): [Position(2,1)],
    Position(2,1): [Position(1,1)],
    Position(1,1): [Position(1,2)],
    Position(1,2): [Position(1,3)],
    Position(1,3): [Position(1,4)],
    Position(1,4): [Position(1,5)],
    Position(1,5): [Position(2,5)],
    Position(2,5): [Position(3,5)],
    Position(3,5): [Position(4,5)],
    Position(4,5): [Position(5,5)],
    Position(5,5): [Position(5,4)],
    Position(5,4): [Position(5,3)],
    Position(5,3): [Position(5,2)],
    Position(5,2): [Position(4,2), Position(5,1)],
    Position(4,2): [Position(3,2)],
    Position(3,2): [Position(2,2)],
    Position(2,2): [Position(2,3)],
    Position(2,3): [Position(2,4)],
    Position(2,4): [Position(3,4)],
    Position(3,4): [Position(4,4)],
    Position(4,4): [Position(4,3)],
    Position(4,3): [Position(3,3), Position(4,2)],
    Position(3,3): [],
}


class PlayerID(Enum):
    Bottom = 0
    Right = 1
    Top = 2
    Left = 3

class Player:
    def __init__(self, id):
        self.id = id
        
        square = Position(6, 3)
        path = BOTTOM_PATH
        for _ in range(self.id.value):
            square = rotate_ccw(square)
            path = rotate_ccw_path(path)
        
        self.starting_square = square
        self.path = path

        self.pieces = []
        for i in range(6):
            self.pieces.append(Piece(self,i))
            
        self.piece_tuples = []

        

    



                
        



    
        