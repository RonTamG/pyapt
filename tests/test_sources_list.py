from pytest import fixture

from src.sources_list import SourcesList


@fixture
def sources_list():
    return """\
    # deb http://deb.debian.org/debian focal main contrib non-free
    deb http://deb.debian.org/debian bullseye main contrib non-free
    deb http://deb.debian.org/debian bullseye-updates main contrib non-free
    deb http://security.debian.org/debian-security bullseye-security main contrib non-free
    """  # noqa: E501


def test_sources_list_returns_release_urls(sources_list):
    expected = [
        "http://deb.debian.org/debian/dists/bullseye/InRelease",
        "http://deb.debian.org/debian/dists/bullseye-updates/InRelease",
        "http://security.debian.org/debian-security/dists/bullseye-security/InRelease",
    ]

    result = SourcesList(sources_list).release_urls()
    assert result == expected


def test_sources_list_returns_index_urls(sources_list):
    expected = [
        "http://deb.debian.org/debian/dists/bullseye/main/binary-amd64/Packages.xz",
        "http://deb.debian.org/debian/dists/bullseye/contrib/binary-amd64/Packages.xz",
        "http://deb.debian.org/debian/dists/bullseye/non-free/binary-amd64/Packages.xz",
        "http://deb.debian.org/debian/dists/bullseye-updates/main/binary-amd64/Packages.xz",
        "http://deb.debian.org/debian/dists/bullseye-updates/contrib/binary-amd64/Packages.xz",
        "http://deb.debian.org/debian/dists/bullseye-updates/non-free/binary-amd64/Packages.xz",
        "http://security.debian.org/debian-security/dists/bullseye-security/main/binary-amd64/Packages.xz",
        "http://security.debian.org/debian-security/dists/bullseye-security/contrib/binary-amd64/Packages.xz",
        "http://security.debian.org/debian-security/dists/bullseye-security/non-free/binary-amd64/Packages.xz",
    ]

    result = SourcesList(sources_list).index_urls(architecture="amd64")
    assert result == expected
