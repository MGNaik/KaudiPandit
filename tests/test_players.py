from src.players import PlayerID, Player
import pytest

@pytest.mark.parametrize("pid", list(PlayerID))
def test_player_stores_id(pid):
        player = Player(pid)
        assert player.id == pid

@pytest.mark.parametrize("pid", list(PlayerID))
def test_player_starting_square_is_set(pid):
        player = Player(pid)
        assert player.starting_square == (6,3)
