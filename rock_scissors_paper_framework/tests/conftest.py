"""Configure pytests."""


def pytest_collection_modifyitems(items):
    """Order so test_default_choices.py runs first."""
    items.sort(key=lambda item: 'test_validate_choices' not in item.nodeid)
