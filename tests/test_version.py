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
        ("2.37-12", "2.4"),
        ("0.9.3+git20220530.e75bdcd-0kali2+b1", "0.9.3+git20220530.e75bdcd~"),
    ],
)
def test_should_compare_greater_than(a, b):
    assert Version(a) > Version(b)


@pytest.mark.parametrize(
    "a, b",
    [
        ("1:0", "2:0"),
        ("0:1-1", "0:2-1"),
        ("0:1-1", "0:1-2"),
        ("0:0-0", "1:0-0"),
        ("11.1+deb11u6", "1:11.1+deb11u6"),
        ("0:a-0", "0:b-0"),
        ("11.1+deb11u6", "11.2+deb11u6"),
        ("0:0-a", "0:0-b"),
        ("1.6.1-5", "1.6.1-5+deb11u1"),
        ("1:16.28.0~dfsg-0+deb11u1", "1:16.28.0~dfsg-0+deb11u2"),
    ],
)
def test_should_compare_less_than(a, b):
    assert Version(a) < Version(b)


def test_should_have_equal_hashes_for_equal_versions():
    version = "11.1+deb11u6"
    assert hash(Version(version)) == hash(Version(version))


def test_should_have_different_hashes_for_different_versions():
    version_1 = "11.1+deb11u6"
    version_2 = "22.2+deb11u6"
    assert hash(Version(version_1)) != hash(Version(version_2))
