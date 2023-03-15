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

