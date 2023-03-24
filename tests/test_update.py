import os

import pytest

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


def test_url_into_saved_file_name():
    urls = ['http://deb.debian.org/debian/dists/bullseye/InRelease',
            'http://deb.debian.org/debian/dists/bullseye/main/binary-amd64/Packages.xz',
            'http://security.debian.org/debian-security/dists/bullseye-security/InRelease',
            'http://security.debian.org/debian-security/dists/bullseye-security/main/binary-amd64/Packages.xz'
            ]

    expected_names = ['deb.debian.org_debian_dists_bullseye_InRelease',
                      'deb.debian.org_debian_dists_bullseye_main_binary-amd64_Packages.xz',
                      'security.debian.org_debian-security_dists_bullseye-security_InRelease',
                      'security.debian.org_debian-security_dists_bullseye-security_main_binary-amd64_Packages.xz'
                      ]

    result = [url_into_saved_file_name(url) for url in urls]

    assert result == expected_names


def test_generate_index_dictionary():
    expected_packages = ['genius', 'genius-common',
                         'genius-dev', 'gnome-genius', 'bart-cuda', 'basilisk2']
    test_indexes = ['main_packages.txt', 'contrib_packages.txt']

    result_packages = {}

    for path in test_indexes:
        with open(os.path.join('tests', 'resources', path), 'r') as index_file:
            data = index_file.read()
        result_packages.update(generate_index_dictionary(data))

    result = [pack in result_packages for pack in expected_packages]
    assert result != []
    assert all(result)


def test_generate_index_dictionary_with_multiline_fields():
    expected = 'interface::graphical, interface::x11, role::program, uitoolkit::gtk, uitoolkit::sdl, x11::application'

    with open(os.path.join('tests', 'resources', 'contrib_packages.txt'), 'r') as index_file:
        data = index_file.read()

    index = generate_index_dictionary(data)

    result = index['basilisk2']['Tag']

    assert result == expected


def test_add_virtual_indexes():
    expected_packages = ['basilisk2', 'bart-cuda', 'bart']

    with open(os.path.join('tests', 'resources', 'contrib_packages.txt'), 'r') as index_file:
        data = index_file.read()

    index = generate_index_dictionary(data)
    result_packages = add_virtual_indexes(index)

    result = [pack in result_packages for pack in expected_packages]
    assert result != []
    assert all(result)


def test_get_apt_sources():
    urls = ['http://deb.debian.org/debian/dists/bullseye/main/binary-amd64/Packages.xz',
            'http://security.debian.org/debian-security/dists/bullseye-security/main/binary-amd64/Packages.xz'
            ]

    expected = ['http://deb.debian.org/debian bullseye/main amd64',
                'http://security.debian.org/debian-security bullseye-security/main amd64'
                ]

    result = [get_apt_sources(url) for url in urls]

    assert result == expected


def test_add_apt_source_field():
    with open(os.path.join('tests', 'resources', 'contrib_packages.txt'), 'r') as index_file:
        data = index_file.read()
    index = generate_index_dictionary(data)

    result = add_apt_source_field(
        index, source='http://deb.debian.org/debian bullseye/main amd64')
    assert all(['Apt-Source' in package for package in result.values()])


@pytest.mark.parametrize('version, expected_epoch, expected_upstream, expected_revision',
                         [
                             ('1:2.30.2-1+deb11u2', '1', '2.30.2', '1+deb11u2'),
                             ('4.7-1', '0', '4.7', '1'),
                             ('0.0.14', '0', '0.0.14', '0'),
                             ('1:8.4p1-5+deb11u1', '1', '8.4p1', '5+deb11u1'),
                             ('3.0043', '0', '3.0043', '0'),
                             ('0.11b-20160615-2', '0', '0.11b-20160615', '2'),
                             ('1:0', '1', '0', '0')
                         ])
def test_split_debian_version(version, expected_epoch, expected_upstream, expected_revision):
    epoch, upstream, revision = split_debian_version(version)

    assert epoch == expected_epoch
    assert upstream == expected_upstream
    assert revision == expected_revision


@pytest.mark.parametrize('a, b, result',
                         [
                             ('1:0', '2:0', -1),
                             ('0:1-1', '0:2-1', -1),
                             ('0:1-1', '0:1-2', -1),
                             # Test for version equality.
                             ('0:0-0', '0:0-0', 0),
                             ('0:0-00', '0:00-0', 0),
                             ('1:2-3', '1:2-3', 0),
                             # Test for epoch difference.
                             ('0:0-0', '1:0-0', -1),
                             ('1:0-0', '0:0-0', 1),
                             ('11.1+deb11u6', '1:11.1+deb11u6', -1),
                             # Test for version component difference.
                             ('0:a-0', '0:b-0', -1),
                             ('0:b-0', '0:a-0', 1),
                             ('11.1+deb11u6', '11.2+deb11u6', -1),
                             ('11.1+deb11u6', '11.1+deb11u6', 0),
                             ('11.1+deb11u6', '11.0+deb11u6', 1),
                             # Test for revision component difference.
                             ('0:0-a', '0:0-b', -1),
                             ('0:0-b', '0:0-a', 1),
                             ('1.6.1-5', '1.6.1-5+deb11u1', -299),
                             ('1:16.28.0~dfsg-0+deb11u1', '1:16.28.0~dfsg-0+deb11u2', -1)
                         ])
def test_compare_debian_version(a, b, result):
    assert dpkg_version_compare(a, b) == result
