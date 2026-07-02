from docs.Rules.src.players import PlayerID, Player
from docs.Rules.src.types import Position
from docs.Rules.src.pieces import Piece
import pytest

@pytest.mark.parametrize("pid", list(PlayerID))
def test_player_stores_id(pid):
        player = Player(pid)
        assert player.id == pid

@pytest.mark.parametrize("pid, expected", [
    (PlayerID.Bottom, Position(6, 3)),
    (PlayerID.Right,  Position(3, 6)),
    (PlayerID.Top,    Position(0, 3)),
    (PlayerID.Left,   Position(3, 0)),
])
def test_player_starting_square(pid, expected):
    
    player = Player(pid)
    assert player.starting_square == expected


def test_player_has_6_pieces():
    player = Player(PlayerID.Bottom)
    assert len(player.pieces) == 6
    for i,piece in enumerate(player.pieces):
        assert isinstance(piece, Piece)
        assert piece.id == i
        assert piece.owner is player
    
     
@pytest.mark.parametrize("pid", list(PlayerID))
def test_player_paths(pid):
    player = Player(pid)
    print()
    print(pid.name)
    for square, nexts in player.path.items():
        print(square, "->", nexts)
        
     


