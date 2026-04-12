from src.board import Board
def test_board_init_empty():
    board_size = 5
    board = Board(board_size)
    assert board.size == board_size
    assert len(board.grid) == board_size
    for r in range(board.size):
        assert len(board.grid[r])== board_size 
        for c in range(board.size):
            assert board.get(r,c) is None
            
    print ("All tests passed!")

