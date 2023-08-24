from src.sources_list import SourcesList


def test_sources_list_returns_index_urls():
    sources_list = """\
        # deb http://deb.debian.org/debian focal main contrib non-free
        deb http://deb.debian.org/debian bullseye main contrib non-free
        deb http://deb.debian.org/debian bullseye-updates main contrib non-free
        deb http://security.debian.org/debian-security bullseye-security main contrib non-free
        """  # noqa: E501

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

    result = SourcesList(sources_list).index_urls(architecture="amd64")
    assert result == expected


def test_sources_list_ignores_commented_lines():
    sources_list = """\
    # deb http://deb.debian.org/debian focal main contrib non-free
    ## deb http://deb.debian.org/debian bullseye main contrib non-free
    deb http://deb.debian.org/debian bullseye-updates main contrib non-free
    deb http://security.debian.org/debian-security bullseye-security main contrib non-free
    """  # noqa: E501

    expected = [
        "http://deb.debian.org/debian/dists/bullseye-updates/main/binary-amd64/Packages",
        "http://deb.debian.org/debian/dists/bullseye-updates/contrib/binary-amd64/Packages",
        "http://deb.debian.org/debian/dists/bullseye-updates/non-free/binary-amd64/Packages",
        "http://security.debian.org/debian-security/dists/bullseye-security/main/binary-amd64/Packages",
        "http://security.debian.org/debian-security/dists/bullseye-security/contrib/binary-amd64/Packages",
        "http://security.debian.org/debian-security/dists/bullseye-security/non-free/binary-amd64/Packages",
    ]

    result = SourcesList(sources_list).index_urls(architecture="amd64")
    assert result == expected


def test_sources_list_ignores_whitespace_lines():
    sources_list = """\
    # deb http://deb.debian.org/debian focal main contrib non-free

    deb http://deb.debian.org/debian bullseye-updates main contrib non-free
    ## deb http://deb.debian.org/debian bullseye main contrib non-free


    deb http://security.debian.org/debian-security bullseye-security main contrib non-free



    """  # noqa: E501

    expected = [
        "http://deb.debian.org/debian/dists/bullseye-updates/main/binary-amd64/Packages",
        "http://deb.debian.org/debian/dists/bullseye-updates/contrib/binary-amd64/Packages",
        "http://deb.debian.org/debian/dists/bullseye-updates/non-free/binary-amd64/Packages",
        "http://security.debian.org/debian-security/dists/bullseye-security/main/binary-amd64/Packages",
        "http://security.debian.org/debian-security/dists/bullseye-security/contrib/binary-amd64/Packages",
        "http://security.debian.org/debian-security/dists/bullseye-security/non-free/binary-amd64/Packages",
    ]

    result = SourcesList(sources_list).index_urls(architecture="amd64")
    assert result == expected
