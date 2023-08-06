import os

import pytest

from src.update import (
    add_apt_source_field,
    add_virtual_indexes,
    dpkg_version_compare,
    generate_index_dictionary,
    get_apt_sources,
    get_index_urls,
    get_release_urls,
    index_to_package_file_format,
    parse_sources_list,
    split_debian_version,
    url_into_saved_file_name,
)


def test_sources_list_parsing():
    sources_list = """\
    # deb http://deb.debian.org/debian focal main contrib non-free
    deb http://deb.debian.org/debian bullseye main contrib non-free
    deb http://deb.debian.org/debian bullseye-updates main contrib non-free
    deb http://security.debian.org/debian-security bullseye-security main contrib non-free
    """  # noqa: E501

    expected = [
        [
            "deb",
            "http://deb.debian.org/debian",
            "bullseye",
            "main",
            "contrib",
            "non-free",
        ],
        [
            "deb",
            "http://deb.debian.org/debian",
            "bullseye-updates",
            "main",
            "contrib",
            "non-free",
        ],
        [
            "deb",
            "http://security.debian.org/debian-security",
            "bullseye-security",
            "main",
            "contrib",
            "non-free",
        ],
    ]

    result = parse_sources_list(sources_list)

    assert result == expected


def test_get_release_urls():
    parts = [
        [
            "deb",
            "http://deb.debian.org/debian",
            "bullseye",
            "main",
            "contrib",
            "non-free",
        ],
        [
            "deb",
            "http://deb.debian.org/debian",
            "bullseye-updates",
            "main",
            "contrib",
            "non-free",
        ],
        [
            "deb",
            "http://security.debian.org/debian-security",
            "bullseye-security",
            "main",
            "contrib",
            "non-free",
        ],
    ]

    expected = [
        "http://deb.debian.org/debian/dists/bullseye/InRelease",
        "http://deb.debian.org/debian/dists/bullseye-updates/InRelease",
        "http://security.debian.org/debian-security/dists/bullseye-security/InRelease",
    ]

    releases = get_release_urls(parts)
    assert releases == expected


def test_get_index_urls():
    parts = [
        [
            "deb",
            "http://deb.debian.org/debian",
            "bullseye",
            "main",
            "contrib",
            "non-free",
        ],
        [
            "deb",
            "http://deb.debian.org/debian",
            "bullseye-updates",
            "main",
            "contrib",
            "non-free",
        ],
        [
            "deb",
            "http://security.debian.org/debian-security",
            "bullseye-security",
            "main",
            "contrib",
            "non-free",
        ],
    ]

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

    result = get_index_urls(parts, architecture="amd64")
    assert result == expected


def test_url_into_saved_file_name():
    urls = [
        "http://deb.debian.org/debian/dists/bullseye/InRelease",
        "http://deb.debian.org/debian/dists/bullseye/main/binary-amd64/Packages.xz",
        "http://security.debian.org/debian-security/dists/bullseye-security/InRelease",
        "http://security.debian.org/debian-security/dists/bullseye-security/main/binary-amd64/Packages.xz",
    ]

    expected_names = [
        "deb.debian.org_debian_dists_bullseye_InRelease",
        "deb.debian.org_debian_dists_bullseye_main_binary-amd64_Packages.xz",
        "security.debian.org_debian-security_dists_bullseye-security_InRelease",
        "security.debian.org_debian-security_dists_bullseye-security_main_binary-amd64_Packages.xz",
    ]

    result = [url_into_saved_file_name(url) for url in urls]

    assert result == expected_names


def test_generate_index_dictionary():
    expected_packages = [
        "genius",
        "genius-common",
        "genius-dev",
        "gnome-genius",
        "bart-cuda",
        "basilisk2",
    ]
    test_indexes = ["main_packages.txt", "contrib_packages.txt"]

    result_packages = {}

    for path in test_indexes:
        with open(os.path.join("tests", "resources", path), "r") as index_file:
            data = index_file.read()
        result_packages.update(generate_index_dictionary(data))

    result = [pack in result_packages for pack in expected_packages]
    assert result != []
    assert all(result)


def test_generate_index_dictionary_with_multiline_fields():
    expected = "interface::graphical, interface::x11, role::program, uitoolkit::gtk, uitoolkit::sdl, x11::application"  # noqa: E501

    with open(
        os.path.join("tests", "resources", "contrib_packages.txt"), "r"
    ) as index_file:
        data = index_file.read()

    index = generate_index_dictionary(data)

    result = index["basilisk2"]["Tag"]

    assert result == expected


def test_generate_index_dictionary_with_multiple_versions():
    expected_packages = ["genius", "genius-common", "genius-dev", "gnome-genius"]
    test_indexes = ["main_packages.txt", "main_packages_other_versions.txt"]

    result_packages = {}

    for path in test_indexes:
        with open(os.path.join("tests", "resources", path), "r") as index_file:
            data = index_file.read()

        for key, value in generate_index_dictionary(data).items():
            if key not in result_packages:
                result_packages[key] = value
            elif (
                dpkg_version_compare(result_packages[key]["Version"], value["Version"])
                < 0
            ):
                result_packages[key] = value

    assert result_packages["gnome-genius"]["Version"] == "2.0.25-2"
    assert result_packages["genius"]["Version"] == "2.0.25-2"

    result = [pack in result_packages for pack in expected_packages]
    assert result != []
    assert all(result)


def test_add_virtual_indexes():
    expected_packages = ["basilisk2", "bart-cuda", "bart"]

    with open(
        os.path.join("tests", "resources", "contrib_packages.txt"), "r"
    ) as index_file:
        data = index_file.read()

    index = generate_index_dictionary(data)
    result_packages = add_virtual_indexes(index)

    result = [pack in result_packages for pack in expected_packages]
    assert result != []
    assert all(result)


def test_get_apt_sources():
    urls = [
        "http://deb.debian.org/debian/dists/bullseye/main/binary-amd64/Packages.xz",
        "http://security.debian.org/debian-security/dists/bullseye-security/main/binary-amd64/Packages.xz",
    ]

    expected = [
        "http://deb.debian.org/debian bullseye/main amd64",
        "http://security.debian.org/debian-security bullseye-security/main amd64",
    ]

    result = [get_apt_sources(url) for url in urls]

    assert result == expected


def test_add_apt_source_field():
    with open(
        os.path.join("tests", "resources", "contrib_packages.txt"), "r"
    ) as index_file:
        data = index_file.read()
    index = generate_index_dictionary(data)

    result = add_apt_source_field(
        index, source="http://deb.debian.org/debian bullseye/main amd64"
    )
    assert all(["Apt-Source" in package for package in result.values()])


@pytest.mark.parametrize(
    "version, expected_epoch, expected_upstream, expected_revision",
    [
        ("1:2.30.2-1+deb11u2", "1", "2.30.2", "1+deb11u2"),
        ("4.7-1", "0", "4.7", "1"),
        ("0.0.14", "0", "0.0.14", "0"),
        ("1:8.4p1-5+deb11u1", "1", "8.4p1", "5+deb11u1"),
        ("3.0043", "0", "3.0043", "0"),
        ("0.11b-20160615-2", "0", "0.11b-20160615", "2"),
        ("1:0", "1", "0", "0"),
    ],
)
def test_split_debian_version(
    version, expected_epoch, expected_upstream, expected_revision
):
    epoch, upstream, revision = split_debian_version(version)

    assert epoch == expected_epoch
    assert upstream == expected_upstream
    assert revision == expected_revision


@pytest.mark.parametrize(
    "a, b, result",
    [
        ("1:0", "2:0", -1),
        ("0:1-1", "0:2-1", -1),
        ("0:1-1", "0:1-2", -1),
        # Test for version equality.
        ("0:0-0", "0:0-0", 0),
        ("0:0-00", "0:00-0", 0),
        ("1:2-3", "1:2-3", 0),
        # Test for epoch difference.
        ("0:0-0", "1:0-0", -1),
        ("1:0-0", "0:0-0", 1),
        ("11.1+deb11u6", "1:11.1+deb11u6", -1),
        # Test for version component difference.
        ("0:a-0", "0:b-0", -1),
        ("0:b-0", "0:a-0", 1),
        ("11.1+deb11u6", "11.2+deb11u6", -1),
        ("11.1+deb11u6", "11.1+deb11u6", 0),
        ("11.1+deb11u6", "11.0+deb11u6", 1),
        # Test for revision component difference.
        ("0:0-a", "0:0-b", -1),
        ("0:0-b", "0:0-a", 1),
        ("1.6.1-5", "1.6.1-5+deb11u1", -299),
        ("1:16.28.0~dfsg-0+deb11u1", "1:16.28.0~dfsg-0+deb11u2", -1),
    ],
)
def test_compare_debian_version(a, b, result):
    assert dpkg_version_compare(a, b) == result


def test_index_can_return_to_package_file():
    with open(
        os.path.join("tests", "resources", "libc6_packages.txt"), "r"
    ) as index_file:
        data = index_file.read()
    index = generate_index_dictionary(data)

    expected = """\
Package: libc6
Source: glibc
Version: 2.31-13+deb11u5
Installed-Size: 12837
Maintainer: GNU Libc Maintainers <debian-glibc@lists.debian.org>
Architecture: amd64
Replaces: libc6-amd64
Depends: libgcc-s1, libcrypt1
Recommends: libidn2-0 (>= 2.0.5~), libnss-nis, libnss-nisplus
Suggests: glibc-doc, debconf | debconf-2.0, libc-l10n, locales
Breaks: busybox (<< 1.30.1-6), hurd (<< 1:0.9.git20170910-1), ioquake3 (<< 1.36+u20200211.f2c61c1~dfsg-2~), iraf-fitsutil (<< 2018.07.06-4), libgegl-0.4-0 (<< 0.4.18), libtirpc1 (<< 0.2.3), locales (<< 2.31), locales-all (<< 2.31), macs (<< 2.2.7.1-3~), nocache (<< 1.1-1~), nscd (<< 2.31), openarena (<< 0.8.8+dfsg-4~), openssh-server (<< 1:8.1p1-5), r-cran-later (<< 0.7.5+dfsg-2), wcc (<< 0.0.2+dfsg-3)
Description: GNU C Library: Shared libraries
Multi-Arch: same
Homepage: https://www.gnu.org/software/libc/libc.html
Description-md5: fc3001b0b90a1c8e6690b283a619d57f
Tag: role::shared-lib
Section: libs
Priority: optional
Filename: pool/main/g/glibc/libc6_2.31-13+deb11u5_amd64.deb
Size: 2825060
MD5sum: 3230125fb2df166e80d7c0de7d148bbb
SHA256: adf6994e4c000ff5b882db411a23925a5860a10146e27fa08fc08cb4d08e6d85\
"""  # noqa: E501

    result = index_to_package_file_format(index["libc6"])
    assert result == expected
