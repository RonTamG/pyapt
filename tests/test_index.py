# ruff: noqa: E501

from pathlib import Path

from src.index import Index
from src.version import Version


def test_index_should_include_package_in_index_file():
    index_file = valid_index_file()

    index = Index(index_file)

    assert len(index) == 1


def test_should_include_all_packages_in_index_file():
    index_file = valid_index_file_with_multiple_packages()

    index = Index(index_file)

    assert len(index) == 2


def test_should_search_packages_by_name():
    index = valid_index()

    package = index.search("python3")

    assert package.name == "python3"


def test_should_contain_multiple_package_versions():
    index_file = valid_index_file_with_multiple_version_of_package()  # noqa: F821

    index = Index(index_file)

    assert len(index.packages.get("python3")) == 3


def test_should_contain_virtual_packages():
    expected = ["python3-profiler", "python3-supported-max", "python3-supported-min"]
    index_file = valid_index_file_with_virtual_packages()

    index = Index(index_file)

    assert all(index.search(pack) is not None for pack in expected)


def test_search_by_name_should_return_latest_version():
    index_file = valid_index_file_with_multiple_version_of_package()  # noqa: F821

    index = Index(index_file)

    assert index.search("python3").version == Version("3.12.4")


def test_should_search_by_name_and_version():
    index_file = valid_index_file_with_multiple_version_of_package()  # noqa: F821

    index = Index(index_file)

    assert index.search("python3 (= 3.11.4-5+b1)").version == Version("3.11.4-5+b1")


def test_should_search_by_later_version():
    index_file = valid_index_file_with_multiple_version_of_package()  # noqa: F821

    index = Index(index_file)

    assert index.search("python3 (>> 3.11.4-5+b1)").version == Version("3.12.4")


def test_should_search_by_earlier_version():
    index_file = valid_index_file_with_multiple_version_of_package()  # noqa: F821

    index = Index(index_file)

    assert index.search("python3 (<< 3.11.4-5+b1)").version == Version("3.10.4")


def test_should_search_by_later_or_equal_version():
    index_file = valid_index_file_with_multiple_version_of_package()  # noqa: F821

    index = Index(index_file)

    assert index.search("python3 (>= 3.11.4-5+b1)").version == Version("3.12.4")

    index = valid_index()

    assert index.search("python3 (>= 3.11.4-5+b1)").version == Version("3.11.4-5+b1")


def test_should_search_by_earlier_or_equal_version():
    index_file = valid_index_file_with_multiple_version_of_package()  # noqa: F821

    index = Index(index_file)

    assert index.search("python3 (<= 3.11.4-5+b1)").version == Version("3.11.4-5+b1")

    assert index.search("python3 (<= 3.10.5)").version == Version("3.10.4")


def test_search_should_pick_first_existing_alternative():
    index = Index(valid_index_file_with_multiple_packages())

    assert index.search("python3 | ca-certificates").name == "python3"
    assert index.search("ca-certificates | python3").name == "ca-certificates"
    assert index.search("doesnt-exist | python3").name == "python3"


def test_should_add_apt_source_field_to_packages():
    source = "http://deb.debian.org/debian bullseye/main amd64"
    index = valid_index()

    index.set_packages_apt_source(source)

    index.search("python3").apt_source = source


def test_should_be_combinable_with_other_indexes():
    index = valid_index()
    index_2 = valid_index_with_other_package()

    index.combine(index_2)

    assert index.search("python3") is not None
    assert index.search("ca-certificates") is not None


def test_should_ignore_architecture_qualifier_if_exists():
    index = valid_index()

    assert index.search("python3:any") is not None
    assert index.search("python3:amd64") is not None
    assert index.search("python3:arm64") is not None


def test_should_check_if_package_is_contained_in_list():
    index = valid_index()

    assert "python3" in index
    assert "python3 (= 3.11.4-5+b1)" in index
    assert "ca-certificates" not in index


def test_should_get_package_dependencies():
    index = valid_full_index_of_package()

    packages = index.get_package_dependencies("python3")

    assert len(packages) == 43


def test_should_get_package_dependencies_with_recommended():
    index = valid_full_index_of_package()

    packages = index.get_package_dependencies("python3", with_recommended=True)

    assert len(packages) == 104


def test_should_get_package_dependencies_should_fail_when_package_is_missing():
    index = full_index_with_missing_package()

    try:
        index.get_package_dependencies("python3")
    except KeyError as e:
        assert str(e) == "'libc6 (>= 2.35)'"
    else:
        raise AssertionError("Expected KeyError but action completed successfully")


def test_should_set_provided_package_version_if_included():
    index = Index(valid_index_file_with_virtual_packages())

    index.search("python3-supported-max (= 3.11)").version == Version("3.11")
    index.search("python3-supported-max").version == Version("3.11")


def valid_index_file():
    return """Package: python3
Source: python3-defaults (3.11.4-5)
Version: 3.11.4-5+b1
Installed-Size: 82
Maintainer: Matthias Klose <doko@debian.org>
Architecture: amd64
Replaces: python3-minimal (<< 3.1.2-2)
Depends: python3.11 (>= 3.11.4-1~), libpython3-stdlib (= 3.11.4-5+b1)
Pre-Depends: python3-minimal (= 3.11.4-5+b1)
Suggests: python3-doc (>= 3.11.4-5+b1), python3-tk (>= 3.11.4-1~), python3-venv (>= 3.11.4-5+b1)
Size: 26464
SHA256: 0249a500d0884183759e63086a81a92e86c6d8592cfca433a87536f985701939
SHA1: ff21b4db2028d765236405ee046acaf75401e5bc
MD5sum: 831af60c5f3f8f4a75315d49c21b0626
Description: interactive high-level object-oriented language (default python3 version) Python, the high-level, interactive object oriented language,
Multi-Arch: allowed
Homepage: https://www.python.org/
Tag: devel::interpreter, devel::lang:python, devel::library, implemented-in::c, implemented-in::python, role::devel-lib,
Section: python
Priority: optional
Filename: ./python3_3.11.4-5+b1_amd64.deb"""


def valid_index_file_with_multiple_packages():
    return """Package: python3
Source: python3-defaults (3.11.4-5)
Version: 3.11.4-5+b1
Installed-Size: 82
Maintainer: Matthias Klose <doko@debian.org>
Architecture: amd64
Replaces: python3-minimal (<< 3.1.2-2)
Depends: python3.11 (>= 3.11.4-1~), libpython3-stdlib (= 3.11.4-5+b1)
Pre-Depends: python3-minimal (= 3.11.4-5+b1)
Suggests: python3-doc (>= 3.11.4-5+b1), python3-tk (>= 3.11.4-1~), python3-venv (>= 3.11.4-5+b1)
Size: 26464
SHA256: 0249a500d0884183759e63086a81a92e86c6d8592cfca433a87536f985701939
SHA1: ff21b4db2028d765236405ee046acaf75401e5bc
MD5sum: 831af60c5f3f8f4a75315d49c21b0626
Description: interactive high-level object-oriented language (default python3 version) Python, the high-level, interactive object oriented language,
Multi-Arch: allowed
Homepage: https://www.python.org/
Tag: devel::interpreter, devel::lang:python, devel::library, implemented-in::c, implemented-in::python, role::devel-lib,
Section: python
Priority: optional
Filename: ./python3_3.11.4-5+b1_amd64.deb

Package: ca-certificates
Version: 20230311
Installed-Size: 384
Maintainer: Julien Cristau <jcristau@debian.org>
Architecture: all
Depends: openssl (>= 1.1.1), debconf (>= 0.5) | debconf-2.0
Enhances: openssl
Breaks: ca-certificates-java (<< 20121112+nmu1)
Size: 153456
SHA256: 5308b9bd88eebe2a48be3168cb3d87677aaec5da9c63ad0cf561a29b8219115c
SHA1: 2723803bd4497bd27a499a249e57936821dedbed
MD5sum: cfc0b4e43c023cdfe87bfa4efac29b6e
Description: Common CA certificates Contains the certificate authorities shipped with Mozilla's browser to allow
Multi-Arch: foreign
Tag: protocol::ssl, role::app-data, security::authentication
Section: misc
Priority: standard
Filename: ./ca-certificates_20230311_all.deb"""


def valid_index_file_with_multiple_version_of_package():
    return "\n\n".join(
        [
            valid_index_file(),
            valid_index_file().replace("Version: 3.11.4-5+b1", "Version: 3.12.4"),
            valid_index_file().replace("Version: 3.11.4-5+b1", "Version: 3.10.4"),
        ]
    )


def valid_index_file_with_virtual_packages():
    return """Package: python3
Source: python3-defaults (3.11.4-5)
Version: 3.11.4-5+b1
Installed-Size: 82
Maintainer: Matthias Klose <doko@debian.org>
Architecture: amd64
Replaces: python3-minimal (<< 3.1.2-2)
Provides: python3-profiler, python3-supported-max (= 3.11), python3-supported-min (= 3.11)
Depends: python3.11 (>= 3.11.4-1~), libpython3-stdlib (= 3.11.4-5+b1)
Pre-Depends: python3-minimal (= 3.11.4-5+b1)
Suggests: python3-doc (>= 3.11.4-5+b1), python3-tk (>= 3.11.4-1~), python3-venv (>= 3.11.4-5+b1)
Size: 26464
SHA256: 0249a500d0884183759e63086a81a92e86c6d8592cfca433a87536f985701939
SHA1: ff21b4db2028d765236405ee046acaf75401e5bc
MD5sum: 831af60c5f3f8f4a75315d49c21b0626
Description: interactive high-level object-oriented language (default python3 version) Python, the high-level, interactive object oriented language,
Multi-Arch: allowed
Homepage: https://www.python.org/
Tag: devel::interpreter, devel::lang:python, devel::library, implemented-in::c, implemented-in::python, role::devel-lib,
Section: python
Priority: optional
Filename: ./python3_3.11.4-5+b1_amd64.deb"""


def valid_index():
    return Index(valid_index_file())


def valid_index_with_other_package():
    data = """Package: ca-certificates
Version: 20230311
Installed-Size: 384
Maintainer: Julien Cristau <jcristau@debian.org>
Architecture: all
Depends: openssl (>= 1.1.1), debconf (>= 0.5) | debconf-2.0
Enhances: openssl
Breaks: ca-certificates-java (<< 20121112+nmu1)
Size: 153456
SHA256: 5308b9bd88eebe2a48be3168cb3d87677aaec5da9c63ad0cf561a29b8219115c
SHA1: 2723803bd4497bd27a499a249e57936821dedbed
MD5sum: cfc0b4e43c023cdfe87bfa4efac29b6e
Description: Common CA certificates Contains the certificate authorities shipped with Mozilla's browser to allow
Multi-Arch: foreign
Tag: protocol::ssl, role::app-data, security::authentication
Section: misc
Priority: standard
Filename: ./ca-certificates_20230311_all.deb"""

    return Index(data)


def valid_full_index_of_package():
    data = Path("tests", "resources", "python_Packages").read_text()
    return Index(data)


def full_index_with_missing_package():
    index = valid_full_index_of_package()
    index.packages.pop("libc6")

    return index
