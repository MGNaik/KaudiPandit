from docs.Rules.src.pieces import Piece
from docs.Rules.src.players import Player, PlayerID
import pytest

@pytest.fixture
def player():
    return Player(PlayerID.Bottom)

def test_piece_stores_owner(player):
    # Create piece from owner and id
    piece = Piece(player, 1)
    # Test owner is creating owner
    assert piece.owner is player

@pytest.mark.parametrize("id", range(6))
def test_piece_stores_id(id,player):
    # Create piece ftrom owner and id
    piece = Piece(player, id)
    # Test piece id is creating id
    assert piece.id == id

def test_piece_inherits_starting_position(player):
    # create piece from owner and Id
    piece = Piece(player, 1)
    # Test piece position is player starting psotiion. 
    assert piece.position == player.starting_square

def test_piece_position_updates(player):
    # create piece from owner and ID
    piece = Piece(player, 1)
    # move piece using update postion method
    piece.position = (3,3)
    # check piece moved to expected square
    assert piece.position == (3,3)

def test_piece_position_can_be_set_to_none(player):
    # create pice from owner and ID
    piece = Piece(player, 1)
    # move piece to None position using update position method
    piece.position = None
    # check piece position is None
    assert piece.position == None

def test_two_pieces_same_owner_are_independent(player):
    # create 6 pieces from owner and ID
    pieces = []
    for id in range(6):
        pieces.append(Piece(player, id))

    pieces[0].position = (3,3)
    assert pieces[0].position == (3,3)
    #loop through and check that none of the instances are the same
    for i in range(1,len(pieces)):
        assert pieces[i].position != pieces[0].position

            




    