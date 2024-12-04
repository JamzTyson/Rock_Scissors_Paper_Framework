"""Tests to validate DEFAULT_CHOICES tuple."""

from collections import defaultdict

import rsp.rsp
from rsp.rsp import DEFAULT_CHOICES


def test_is_tuple():
    """DEFAULT_CHOICES should be a tuple."""
    assert isinstance(DEFAULT_CHOICES, tuple)


def test_choice_strings():
    """Each item in DEFAULT_CHOICES must be a string value."""
    for choice in DEFAULT_CHOICES:
        assert isinstance(choice, str)


def test_length():
    """Number of choices must be greater than 1."""
    assert len(DEFAULT_CHOICES) > 1


def test_odd_number():
    """Number of choices must be odd."""
    assert len(DEFAULT_CHOICES) % 2 == 1


def test_not_start_with_q():
    """No choice can begin with QUIT_KEY (default: 'Q')."""
    for choice in DEFAULT_CHOICES:
        assert not choice[0].upper() == rsp.rsp.QUIT_KEY, f"Bad option: {choice}"


def test_not_start_with_space():
    """No choice can begin with a space."""
    for choice in DEFAULT_CHOICES:
        assert not choice[0] == ' ', f"Bad option: {choice}"


def test_no_empty_names():
    """No choice can be an empty string."""
    for choice in DEFAULT_CHOICES:
        assert choice != '', "Bad option: Empty string"


def test_unique_first_letter():
    """Each choice must have a unique first letter (case-insensitive)."""
    first_letters = defaultdict(list)
    for choice in DEFAULT_CHOICES:
        first_letters[choice[0].upper()].append(choice)
    duplicates = {k: v for k, v in first_letters.items() if len(v) > 1}
    assert len(duplicates) == 0, f"Duplicate first letters found: {duplicates}"
