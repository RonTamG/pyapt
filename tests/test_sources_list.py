from src.sources_list import SourcesList


def test_sources_list_returns_index_urls():
    sources_list, expected = valid_sources_list()

    result = SourcesList(sources_list).index_urls(architecture="amd64")

    assert all(item in result for item in expected)


def test_sources_list_with_commented_lines_ignores_them():
    sources_list, expected = sources_list_with_commented_lines()

    result = SourcesList(sources_list).index_urls(architecture="amd64")

    assert all(item in result for item in expected)


def test_sources_list_with_whitespace_ignores_it():
    sources_list, expected = sources_list_with_whitespace()

    result = SourcesList(sources_list).index_urls(architecture="amd64")

    assert all(item in result for item in expected)


def valid_sources_list():
    sources_list = """\
deb http://deb.debian.org/debian bullseye main contrib non-free
deb http://deb.debian.org/debian bullseye-updates main contrib non-free
deb http://security.debian.org/debian-security bullseye-security main contrib non-free
"""
    expected = [
        "http://deb.debian.org/debian/dists/bullseye/main/binary-amd64/Packages",
        "http://deb.debian.org/debian/dists/bullseye/contrib/binary-amd64/Packages",
        "http://deb.debian.org/debian/dists/bullseye/non-free/binary-amd64/Packages",
        "http://deb.debian.org/debian/dists/bullseye-updates/main/binary-amd64/Packages",
        "http://deb.debian.org/debian/dists/bullseye-updates/contrib/binary-amd64/Packages",
        "http://deb.debian.org/debian/dists/bullseye-updates/non-free/binary-amd64/Packages",
        "http://security.debian.org/debian-security/dists/bullseye-security/main/binary-amd64/Packages",
        "http://security.debian.org/debian-security/dists/bullseye-security/contrib/binary-amd64/Packages",
        "http://security.debian.org/debian-security/dists/bullseye-security/non-free/binary-amd64/Packages",
    ]
    return sources_list, expected


def sources_list_with_commented_lines():
    sources_list = """\
#deb http://deb.debian.org/debian bullseye main contrib non-free
# deb http://deb.debian.org/debian bullseye-updates main contrib non-free
deb http://security.debian.org/debian-security bullseye-security main contrib non-free
"""
    expected = [
        "http://security.debian.org/debian-security/dists/bullseye-security/main/binary-amd64/Packages",
        "http://security.debian.org/debian-security/dists/bullseye-security/contrib/binary-amd64/Packages",
        "http://security.debian.org/debian-security/dists/bullseye-security/non-free/binary-amd64/Packages",
    ]

    return sources_list, expected


def sources_list_with_whitespace():
    sources_list = """\
# deb http://deb.debian.org/debian focal main contrib non-free

deb http://deb.debian.org/debian bullseye-updates main contrib non-free
## deb http://deb.debian.org/debian bullseye main contrib non-free


deb http://security.debian.org/debian-security bullseye-security main contrib non-free

"""
    expected = [
        "http://deb.debian.org/debian/dists/bullseye-updates/main/binary-amd64/Packages",
        "http://deb.debian.org/debian/dists/bullseye-updates/contrib/binary-amd64/Packages",
        "http://deb.debian.org/debian/dists/bullseye-updates/non-free/binary-amd64/Packages",
        "http://security.debian.org/debian-security/dists/bullseye-security/main/binary-amd64/Packages",
        "http://security.debian.org/debian-security/dists/bullseye-security/contrib/binary-amd64/Packages",
        "http://security.debian.org/debian-security/dists/bullseye-security/non-free/binary-amd64/Packages",
    ]

    return sources_list, expected
