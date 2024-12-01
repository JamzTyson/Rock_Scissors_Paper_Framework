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


@pytest.mark.parametrize("choices", ('Abc', 'Def', 'Ghi'))
def test_map_initial_to_name_caching(choices):
    """Test map_initial_to_name caches its results."""
    first_result = rsp.map_initial_to_name(choices)
    cached_result = rsp.map_initial_to_name(choices)
    assert cached_result is first_result, "The result was not cached."
