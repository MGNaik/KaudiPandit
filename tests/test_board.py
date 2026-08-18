from src.board import Board
from src.types import Position, Square

safe_positions = {Position(0, 0), Position(0, 3), Position(0, 6),
                      Position(2, 2), Position(2, 4),
                      Position(3, 0), Position(3, 3), Position(3, 6),
                      Position(4, 2), Position(4, 4),
                      Position(6, 0), Position(6, 3), Position(6, 6)}
final_position = Position(3, 3)

def test_board_size_is_7x7():
    board = Board()
    assert len(board.grid) == 7
    for row in board.grid:
        assert len(row)== 7

def test_board_elements_are_squares():
    board = Board()
    for row in board.grid: 
        for square in row:
            assert isinstance(square,Square)

def test_board_safe_and_final_squares():
    board = Board()
    for row in board.grid: 
        for square in row:
            if square.position in safe_positions:
                assert square.safe == True
            else:
                assert square.safe == False

            if square.position == final_position:
                assert square.is_final == True
            else:
                assert square.is_final == False


