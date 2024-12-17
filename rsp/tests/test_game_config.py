"""Unit tests for game logic."""

import pytest

from rsp.rsp import GameOptions
from rsp.tests.config_data import valid_data, invalid_data


@pytest.mark.parametrize('choice_names, expected_exception', invalid_data())
def test_invalid_choices(choice_names, expected_exception):
    """Check that GameOptions raises an error for invalid choices."""
    with pytest.raises(expected_exception):
        GameOptions(choice_names)


@pytest.mark.parametrize("choice_names, expected_names", valid_data())
def test_names(choice_names, expected_names):
    """GameOptions.choices matches initialization argument."""
    config = GameOptions(choice_names)
    assert config.names == expected_names['choices']


@pytest.mark.parametrize("choices, expected", valid_data())
def test_choice_keys(choices, expected):
    """Each choice is beaten by half of the other choices.

    Where the number of choices = n, each choice beats (n - 1) / 2 choices.
    It can be assumed that n is an odd number (tested elsewhere).
    For a choice index 'i', the beaten choices are `i-1` to `i-(n-1)/2`.

    Args:
        choices (HandNames): The choices used to initialse GameCofig.
        expected (dict): Mapping of choices to the choices it beats.
    """
    config = GameOptions(choices)
    assert config.choice_keys == expected['choice_keys']


def test_names_immutable():
    """Ensure that 'names' cannot be modified after initialization."""
    config = GameOptions(('Rock', 'Paper', 'Scissors'))

    with pytest.raises(AttributeError):
        config.names = ('Lizard', 'Spock')


def test_choice_keys_immutable():
    """Ensure that 'choice_keys' cannot be modified after initialization."""
    config = GameOptions(('Rock', 'Paper', 'Scissors'))

    with pytest.raises(AttributeError):
        config.choice_keys = ['R', 'P', 'L']
