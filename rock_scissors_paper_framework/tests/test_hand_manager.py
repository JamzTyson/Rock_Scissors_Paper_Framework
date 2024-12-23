"""Unit tests for HandManager() class."""
from typing import Any

import pytest

from ..rsp import GameOptions, Hand, HandManager
from ..tests.config_data import valid_data


@pytest.fixture
def hand_manager(request):
    """Fixture creates instance of HandManager."""
    game_options = GameOptions(request.param)
    return HandManager(game_options)


@pytest.mark.parametrize("hand_manager, expected", valid_data(),
                         indirect=['hand_manager'])
# pylint: disable=W0621
def test_hands(hand_manager: HandManager, expected: dict[str, Any]):
    """Validate HandManage().hands."""
    assert isinstance(hand_manager.hands, list)
    # Ensure that there is one hand per name and per choice_key.
    assert (len(hand_manager.hands) ==
            len(expected['valid_HandNames']) ==
            len(expected['choice_keys']))
    for name, key, hand in zip(expected['valid_HandNames'],
                               expected['choice_keys'],
                               hand_manager.hands):
        assert isinstance(hand, Hand)
        assert hand.name == name
        assert hand.choice_key == key
