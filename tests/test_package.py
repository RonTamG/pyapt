# ruff: noqa: E501

from src.package import Package
from src.version import Version


def test_should_have_a_name():
    package_data = valid_package_data()

    package = Package(package_data)

    assert package.name == "python3"


def test_should_have_a_version():
    package_data = valid_package_data()

    package = Package(package_data)

    assert package.version == Version("3.11.4-5+b1")


def test_should_have_an_architecture_field():
    package_data = valid_package_data()

    package = Package(package_data)

    assert package.architecture == "amd64"


def test_should_have_a_maintainer_field():
    package_data = valid_package_data()

    package = Package(package_data)

    assert package.maintainer == "Matthias Klose <doko@debian.org>"


def test_should_have_a_description():
    package_data = valid_package_data()

    package = Package(package_data)

    assert (
        package.description
        == "interactive high-level object-oriented language (default python3 version) Python, the high-level, interactive object oriented language,"
    )


def valid_package_data():
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
