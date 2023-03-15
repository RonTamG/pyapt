from src.update import *


def test_sources_list_parsing():
    sources_list = '''\
    # deb http://deb.debian.org/debian focal main contrib non-free
    deb http://deb.debian.org/debian bullseye main contrib non-free
    deb http://deb.debian.org/debian bullseye-updates main contrib non-free
    deb http://security.debian.org/debian-security bullseye-security main contrib non-free
    '''

    expected = [
        ['deb', 'http://deb.debian.org/debian',
            'bullseye', 'main', 'contrib', 'non-free'],
        ['deb', 'http://deb.debian.org/debian',
         'bullseye-updates', 'main', 'contrib', 'non-free'],
        ['deb', 'http://security.debian.org/debian-security',
         'bullseye-security', 'main', 'contrib', 'non-free']
    ]

    result = parse_sources_list(sources_list)

    assert result == expected


def test_get_release_urls():
    parts = [
        ['deb', 'http://deb.debian.org/debian',
            'bullseye', 'main', 'contrib', 'non-free'],
        ['deb', 'http://deb.debian.org/debian',
         'bullseye-updates', 'main', 'contrib', 'non-free'],
        ['deb', 'http://security.debian.org/debian-security',
         'bullseye-security', 'main', 'contrib', 'non-free']
    ]

    expected = [
        'http://deb.debian.org/debian/dists/bullseye/InRelease',
        'http://deb.debian.org/debian/dists/bullseye-updates/InRelease',
        'http://security.debian.org/debian-security/dists/bullseye-security/InRelease'
    ]

    releases = get_release_urls(parts)
    assert releases == expected


def test_get_index_urls():
    parts = [
        ['deb', 'http://deb.debian.org/debian',
            'bullseye', 'main', 'contrib', 'non-free'],
        ['deb', 'http://deb.debian.org/debian',
         'bullseye-updates', 'main', 'contrib', 'non-free'],
        ['deb', 'http://security.debian.org/debian-security',
         'bullseye-security', 'main', 'contrib', 'non-free']
    ]

    expected = [
        'http://deb.debian.org/debian/dists/bullseye/main/binary-amd64/Packages.xz',
        'http://deb.debian.org/debian/dists/bullseye/contrib/binary-amd64/Packages.xz',
        'http://deb.debian.org/debian/dists/bullseye/non-free/binary-amd64/Packages.xz',
        'http://deb.debian.org/debian/dists/bullseye-updates/main/binary-amd64/Packages.xz',
        'http://deb.debian.org/debian/dists/bullseye-updates/contrib/binary-amd64/Packages.xz',
        'http://deb.debian.org/debian/dists/bullseye-updates/non-free/binary-amd64/Packages.xz',
        'http://security.debian.org/debian-security/dists/bullseye-security/main/binary-amd64/Packages.xz',
        'http://security.debian.org/debian-security/dists/bullseye-security/contrib/binary-amd64/Packages.xz',
        'http://security.debian.org/debian-security/dists/bullseye-security/non-free/binary-amd64/Packages.xz'
    ]

    result = get_index_urls(parts, architecture='amd64')
    assert result == expected


