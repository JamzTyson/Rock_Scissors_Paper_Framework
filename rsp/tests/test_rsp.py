"""Unit tests for game logic."""
import pytest

from rsp import rsp


@pytest.mark.parametrize(
    "test_input,expected", [
        # Default test.
        (('Rock', 'Paper', 'Scissors'),
         {'r': 'Rock', 'p': 'Paper', 's': 'Scissors'}),
        # Mixed  case names.
        (('aaA', 'BBB', 'Ccc', 'dDD'),
         {'a': 'aaA', 'b': 'BBB', 'c': 'Ccc', 'd': 'dDD'}),
        # Empty test_input.
        (tuple(), dict()),
        # Single name.
        (('Rock',), {'r': 'Rock'}),
        # Numeric characters.
        (('123', '456', '789'), {'1': '123', '4': '456', '7': '789'}),
        # Names with spaces.
        (('Hello World', 'a b c'), {'h': 'Hello World', 'a': 'a b c'})
    ]
)
def test_map_initial_to_name(test_input, expected):
    """Test initial letter of choices mapped to full names."""
    assert rsp.map_initial_to_name(test_input) == expected


def test_map_initial_to_name_caching():
    """Test map_initial_to_name caches its results."""
    choices = ('Abc', 'Def', 'Ghi')
    first_result = rsp.map_initial_to_name(choices)
    cached_result = rsp.map_initial_to_name(choices)
    assert cached_result is first_result, "The result was not cached."


@pytest.mark.parametrize(
    'choices, expected', [
        # Default test.
        (('Rock', 'Paper', 'Scissors'), '[R]ock, [P]aper, [S]cissors'),
        # Mixed  case names.
        (('aaA', 'BBB', 'Ccc', 'dDD'), '[A]aA, [B]BB, [C]cc, [D]DD'),
        # Empty test_input.
        (tuple(), ''),
        # Single name.
        (('Rock',), '[R]ock'),
        # Numeric characters.
        (('123', '456', '789'), '[1]23, [4]56, [7]89'),
        # Names with spaces.
        (('Hello World', 'a b c'), '[H]ello World, [A] b c')
    ]
)
def test_formatted_choices(choices, expected):
    """Test return value matches format '[R]ock, [P]aper, [S]cissors'."""
    rsp.formatted_choices.cache_clear()
    assert rsp.formatted_choices(choices) == expected


def test_formatted_choices_caching():
    """Test map_initial_to_name caches its results."""
    choices = ('Abc', 'Def', 'Ghi')
    first_result = rsp.formatted_choices(choices)
    cached_result = rsp.formatted_choices(choices)
    assert cached_result is first_result, "The result was not cached."


@pytest.mark.parametrize(
    'choices, expected', [
        # Default test.
        (('Rock', 'Paper', 'Scissors'), "'R', 'P', 'S'"),
        # Mixed  case names.
        (('aaA', 'BBB', 'Ccc', 'dDD'), "'A', 'B', 'C', 'D'"),
        # Empty test_input.
        (tuple(), ''),
        # Single name.
        (('Rock',), "'R'"),
        # Numeric characters.
        (('123', '456', '789'), "'1', '4', '7'"),
        # Names with spaces.
        (('Hello World', 'a b c'), "'H', 'A'")
    ]
)
def test_formatted_input_choices(choices, expected):
    """Test that formatted_input_choices() returns formatted first letters.

    The returned string should be in the form: "'R', 'P', 'S'"
    """
    rsp.formatted_input_choices.cache_clear()
    assert rsp.formatted_input_choices(choices) == expected


def test_formatted_input_choices_caching():
    """Test map_initial_to_name caches its results."""
    choices = ('Abc', 'Def', 'Ghi')
    first_result = rsp.formatted_input_choices(choices)
    cached_result = rsp.formatted_input_choices(choices)
    assert cached_result is first_result, "The result was not cached."
