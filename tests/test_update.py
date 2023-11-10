import os
from pathlib import Path

import pytest

from src.update import (
    add_apt_source_field,
    add_virtual_indexes,
    dpkg_version_compare,
    generate_index_dictionary,
    get_apt_sources,
    index_to_package_file_format,
    split_debian_version,
)


def full_index_data():
    with open(
        Path("tests", "resources", "python_Packages"), "r", encoding="utf-8"
    ) as index_file:
        return index_file.read()


def index_data_with_multiline_field():
    index_data = full_index_data()
    return index_data.replace(
        "Depends: python3.11 (>= 3.11.4-1~), libpython3-stdlib (= 3.11.4-5+b1)",
        "Depends: python3.11 (>= 3.11.4-1~),\n libpython3-stdlib (= 3.11.4-5+b1)",
    )


def genius_version_1_package_data():
    return """\
Package: genius
Version: 1.0.25-2
Installed-Size: 774
Maintainer: Felipe Sateler <fsateler@debian.org>
Architecture: amd64
Depends: libc6 (>= 2.14), libglib2.0-0 (>= 2.35.9), libgmp10, libmpfr6 (>= 3.1.3), libreadline8 (>= 6.0), libtinfo6 (>= 6), genius-common (>= 1.0.25-2), genius-common (<= 1.0.25-2.)
Description: advanced general purpose calculator program (CLI frontend)
Homepage: https://www.5z.com/jirka/genius.html
Description-md5: 91ce686a0384efccfc97b0de617f8732
Tag: field::mathematics, role::program, uitoolkit::ncurses
Section: gnome
Priority: optional
Filename: pool/main/g/genius/genius_1.0.25-2_amd64.deb
Size: 348540
MD5sum: a0521c13eb57afa16d9c5aa4cef01100
SHA256: c7d6931b92e4902814e59194a16c3936d8622eda2cb5cfc222ee17ae99bb7f82
"""  # noqa: E501


def genius_version_2_package_data():
    return """\
Package: genius
Version: 2.0.25-2
Installed-Size: 774
Maintainer: Felipe Sateler <fsateler@debian.org>
Architecture: amd64
Depends: libc6 (>= 2.14), libglib2.0-0 (>= 2.35.9), libgmp10, libmpfr6 (>= 3.1.3), libreadline8 (>= 6.0), libtinfo6 (>= 6), genius-common (>= 1.0.25-2), genius-common (<= 1.0.25-2.)
Description: advanced general purpose calculator program (CLI frontend)
Homepage: https://www.5z.com/jirka/genius.html
Description-md5: 91ce686a0384efccfc97b0de617f8732
Tag: field::mathematics, role::program, uitoolkit::ncurses
Section: gnome
Priority: optional
Filename: pool/main/g/genius/genius_2.0.25-2_amd64.deb
Size: 348540
MD5sum: a0521c13eb57afa16d9c5aa4cef01100
SHA256: c7d6931b92e4902814e59194a16c3936d8622eda2cb5cfc222ee17ae99bb7f82
"""  # noqa: E501


def genius_package_data_with_provides_field():
    data = genius_version_2_package_data()
    return data + "Provides: genius_virtual\n"


def package_file_urls_with_sources():
    urls = [
        "http://deb.debian.org/debian/dists/bullseye/main/binary-amd64/Packages.xz",
        "http://security.debian.org/debian-security/dists/bullseye-security/main/binary-amd64/Packages.xz",
    ]
    expected = [
        "http://deb.debian.org/debian bullseye/main amd64",
        "http://security.debian.org/debian-security bullseye-security/main amd64",
    ]

    return urls, expected


def valid_index():
    return generate_index_dictionary(full_index_data())


def test_full_index_data_generates_full_index_dictionary():
    index_data = full_index_data()

    result = generate_index_dictionary(index_data)

    assert len(result) == 103


def test_index_data_with_multiline_fields_combines_the_lines():
    index_data = index_data_with_multiline_field()

    index = generate_index_dictionary(index_data)
    result = index["python3"]["Depends"]

    assert result == "python3.11 (>= 3.11.4-1~), libpython3-stdlib (= 3.11.4-5+b1)"


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


def test_index_can_have_virtual_packages_added_according_to_provider_fields():
    index_data = genius_package_data_with_provides_field()

    index = generate_index_dictionary(index_data)
    result = add_virtual_indexes(index)

    assert "genius_virtual" in result


def test_package_file_urls_can_be_converted_to_original_apt_source():
    package_urls, expected_sources = package_file_urls_with_sources()

    result = [get_apt_sources(url) for url in package_urls]

    assert all(item in result for item in expected_sources)


def test_index_adding_apt_source_field_is_successful():
    index = valid_index()
    source = "http://deb.debian.org/debian bullseye/main amd64"

    result = add_apt_source_field(index, source=source)

    assert all(["Apt-Source" in package for package in result.values()])
    assert all([package["Apt-Source"] == source for package in result.values()])


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
def test_debian_version_split_into_base_parts_is_successfull(
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
def test_debian_version_compare_is_successfull(a, b, result):
    assert dpkg_version_compare(a, b) == result


def test_index_can_return_to_package_file():
    expected = genius_version_1_package_data().strip()
    index = generate_index_dictionary(expected)

    result = index_to_package_file_format(index["genius"])

    assert result == expected
