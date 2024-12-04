"""Unit tests for game logic."""

import pytest

from rsp.rsp import GameConfig


def data():
    """Test configurations and expected results.


    """
    return [
        # Default test.
        (GameConfig(('Rock', 'Paper', 'Scissors')),
         {
             'choices': ('Rock', 'Paper', 'Scissors'),
             'choice_map': {'R': 'Rock', 'P': 'Paper', 'S': 'Scissors'},
             'formatted_choices': '[R]ock, [P]aper, [S]cissors',
             'user_input_choices': "'R', 'P', 'S'"
         }
         ),
        # Mixed case names.
        (GameConfig(('aaA', 'BBB', 'Ccc', 'dDD')),
         {
             'choices': ('aaA', 'BBB', 'Ccc', 'dDD'),
             'choice_map': {'A': 'aaA', 'B': 'BBB', 'C': 'Ccc', 'D': 'dDD'},
             'formatted_choices': '[A]aA, [B]BB, [C]cc, [D]DD',
             'user_input_choices': "'A', 'B', 'C', 'D'"
         }
         ),
        # Empty test_input.
        (GameConfig(tuple()),
         {
             'choices': tuple(),
             'choice_map': {},
             'formatted_choices': '',
             'user_input_choices': ''
         }
         ),
        # Single name.
        (GameConfig(('Rock',)),
         {
             'choices': ('Rock',),
             'choice_map': {'R': 'Rock'},
             'formatted_choices': '[R]ock',
             'user_input_choices': "'R'"
         }
         ),
        # Numeric characters.
        (GameConfig(('123', '456', '789')),
         {
             'choices': ('123', '456', '789'),
             'choice_map': {'1': '123', '4': '456', '7': '789'},
             'formatted_choices': '[1]23, [4]56, [7]89',
             'user_input_choices': "'1', '4', '7'"
         }
         ),
        # Names with spaces.
        (GameConfig(('Hello World', 'a b c')),
         {
             'choices': ('Hello World', 'a b c'),
             'choice_map': {'H': 'Hello World', 'A': 'a b c'},
             'formatted_choices': '[H]ello World, [A] b c',
             'user_input_choices': "'H', 'A'"
         }
         )
    ]


@pytest.mark.parametrize("config, expected", data())
def test_choices(config, expected):
    """GameConfig.choices matches initialization argument."""
    assert config.choices == expected['choices']


@pytest.mark.parametrize("config, expected", data())
def test_choice_map(config, expected):
    """Uppercase initial letter of choices mapped to full names."""
    assert config.choice_map == expected['choice_map']


@pytest.mark.parametrize("config, expected", data())
def test_formatted_choices(config, expected):
    """Return value matches format '[R]ock, [P]aper, [S]cissors'."""
    assert config.formatted_choices == expected['formatted_choices']


@pytest.mark.parametrize("config, expected", data())
def test_user_input_choices(config, expected):
    """Formatted_input_choices() returns formatted first letters.

    The returned string is in the form: "'R', 'P', 'S'"
    """
    assert config.user_input_choices == expected['user_input_choices']
