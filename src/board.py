from docs.Rules.src.types import Square, Position
class Board: 

    safe_positions = {Position(0, 0), Position(0, 3), Position(0, 6),
                      Position(2, 2), Position(2, 4),
                      Position(3, 0), Position(3, 3), Position(3, 6),
                      Position(4, 2), Position(4, 4),
                      Position(6, 0), Position(6, 3), Position(6, 6)}
    final_position = Position(3, 3)

    def __init__(self, size=7):
        self.size = size

        self.grid = [
            [Square(Position(r,c),
                    safe = (Position(r,c) in self.safe_positions),
                    is_final = (Position(r,c) == self.final_position)              
            ) for c in range(self.size) ]
            for r in range(self.size)
        ]

    
    def get(self,row,col):
        return self.grid[row][col]










