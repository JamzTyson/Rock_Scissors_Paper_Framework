"""Unit tests for the UI class.

These tests focus on verifying the logic of the UI methods.
Terminal-specific behavior, such as clearing the screen,
is irrelevant in automated test environments and is not tested.
Implementation specific strings are not unit tested.
"""


from unittest.mock import patch

import pytest

from ..rsp import GameOptions, UI
from ..tests.config_data import valid_data


@pytest.fixture
def display_manager():
    """Fixture to create a UI instance."""
    def _create_display_manager(choice_names=('Rock', 'Paper', 'Scissors')):
        config = GameOptions(choice_names)
        return UI(config)
    return _create_display_manager


@pytest.mark.parametrize("choice_names, expected", valid_data())
# pylint: disable=W0621
def test_name(choice_names, expected, display_manager):
    """UI.names matches validated Hand names."""
    dm = display_manager(choice_names)
    assert dm.names == expected['valid_HandNames']


def test_get_user_input(display_manager):  # pylint: disable=W0621
    """User input must be stripped and converted to uppercase."""
    user_input = '  hello world  '
    expected = 'HELLO WORLD'
    with patch('builtins.input', return_value=user_input):
        dm = display_manager()
        result = dm.get_user_input()
        assert result == expected, f"Expected {expected}, but got {result}"
