import pytest

from src.version import Version


@pytest.mark.parametrize(
    "a, b",
    [
        ("0:0-0", "0:0-0"),
        ("0:0-00", "0:00-0"),
        ("1:2-3", "1:2-3"),
        ("11.1+deb11u6", "11.1+deb11u6"),
    ],
)
def test_should_compare_equal(a, b):
    assert Version(a) == Version(b)


@pytest.mark.parametrize(
    "a, b",
    [
        ("1:0-0", "0:0-0"),
        ("0:b-0", "0:a-0"),
        ("11.1+deb11u6", "11.0+deb11u6"),
        ("0:0-b", "0:0-a"),
    ],
)
def test_should_compare_greater_than(a, b):
    assert Version(a) > Version(b)
