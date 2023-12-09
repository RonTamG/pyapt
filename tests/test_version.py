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
