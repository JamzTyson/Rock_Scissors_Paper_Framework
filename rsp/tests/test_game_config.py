"""Unit tests for game logic."""

import pytest

from rsp.rsp import GameOptions


@pytest.mark.parametrize(
    "choices, expected_exception",
    [
        ((), ValueError),
        ({'rock', 'scissors', 'paper'}, TypeError),
        (('rock', 'scissors', 42), TypeError),
        (('Rock',), ValueError),
        (('Rock', 'Paper'), ValueError),
        (('Rock', 'Paper', 'Scissors', 'Lizard'), ValueError),
        (('rock', 'Rock', 'Paper'), ValueError),
        (('Rock', 'Paper', 'Scissors', 'Lizard', 'Superman'), ValueError)
    ]
)
def test_invalid_choices(choices, expected_exception):
    """Check that GameOptions raises an error for invalid choices."""
    with pytest.raises(expected_exception) as exc:
        GameOptions(choices)
    print(f"Raised exception message: {exc.value}")


def valid_data():
    """Test configurations and expected results."""
    return [
        # Default test.
        (GameOptions(('Rock', 'Paper', 'Scissors')),
         {
             'choices': ('Rock', 'Paper', 'Scissors'),
             'choice_map': {'R': 'Rock', 'P': 'Paper', 'S': 'Scissors'},
             'formatted_choices': '[R]ock, [P]aper, [S]cissors',
             'user_input_choices': "'R', 'P', 'S'"
         }
         ),
        # Mixed case names.
        (GameOptions(('aaA', 'BBB', 'Ccc', 'dDD', 'eee')),
         {
             'choices': ('aaA', 'BBB', 'Ccc', 'dDD', 'eee'),
             'choice_map': {'A': 'aaA', 'B': 'BBB', 'C': 'Ccc', 'D': 'dDD', 'E': 'eee'},
             'formatted_choices': '[A]aA, [B]BB, [C]cc, [D]DD, [E]ee',
             'user_input_choices': "'A', 'B', 'C', 'D', 'E'"
         }
         ),
        # Numeric characters.
        (GameOptions(('123', '456', '789')),
         {
             'choices': ('123', '456', '789'),
             'choice_map': {'1': '123', '4': '456', '7': '789'},
             'formatted_choices': '[1]23, [4]56, [7]89',
             'user_input_choices': "'1', '4', '7'"
         }
         ),
        # Names with spaces or special characters.
        (GameOptions(('Hello World', 'a b c', '&£$*%-_')),
         {
             'choices': ('Hello World', 'a b c', '&£$*%-_'),
             'choice_map': {'H': 'Hello World', 'A': 'a b c', '&': '&£$*%-_'},
             'formatted_choices': '[H]ello World, [A] b c, [&]£$*%-_',
             'user_input_choices': "'H', 'A', '&'"
         }
         )
    ]


@pytest.mark.parametrize("config, expected", valid_data())
def test_choices(config, expected):
    """GameOptions.choices matches initialization argument."""
    assert config.names == expected['choices']


@pytest.mark.parametrize("config, expected", valid_data())
def test_choice_map(config, expected):
    """Uppercase initial letter of choices mapped to full names."""
    assert config.choice_map == expected['choice_map']


@pytest.mark.parametrize("config, expected", valid_data())
def test_formatted_choices(config, expected):
    """Return value matches format '[R]ock, [P]aper, [S]cissors'."""
    assert config.formatted_choices == expected['formatted_choices']


@pytest.mark.parametrize("config, expected", valid_data())
def test_user_input_choices(config, expected):
    """Formatted_input_choices() returns formatted first letters.

    The returned string is in the form: "'R', 'P', 'S'"
    """
    assert config.formatted_user_input_choices == expected['user_input_choices']


@pytest.mark.parametrize(
    "choices, expected",
    [
        # Default choices (Rock, Paper, Scissors)
        (('Rock', 'Paper', 'Scissors'),
         {'Paper': ['Rock'], 'Rock': ['Scissors'], 'Scissors': ['Paper']}),

        # Extended choices (Rock, Batman, Paper, Lizard, Scissors)
        (('Rock', 'Batman', 'Paper', 'Lizard', 'Scissors'),
         {
             'Rock': ['Scissors', 'Lizard'],
             'Batman': ['Rock', 'Scissors'],
             'Paper': ['Batman', 'Rock'],
             'Lizard': ['Paper', 'Batman'],
             'Scissors': ['Lizard', 'Paper']
         }),
    ]
)
def test_is_beaten_by(choices, expected):
    """Each choice is beaten by half of the other choices.

    Where the number of choices = n, each choice beats (n - 1) / 2 choices.
    It can be assumed that n is an odd number (tested elsewhere).
    For a choice index 'i', the beaten choices are `i-1` to `i-(n-1)/2`.

    Args:
        choices (HandNames): The choices used to initialse GameCofig.
        expected (dict): Mapping of choices to the choices it beats.
    """
    config = GameOptions(choices)
    assert config.is_beaten_by == expected
