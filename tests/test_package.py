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


def test_should_have_priority_optional_if_none_specified():
    package = Package(valid_package_data())

    assert package.priority == "optional"


def test_should_have_priority_field():
    package = Package(valid_package_data_with_priority_field())

    assert package.priority == "required"


def test_new_package_should_have_a_none_apt_source_field():
    package_data = valid_package_data()

    package = Package(package_data)

    assert package.apt_source is None


def test_should_be_compareable_by_name():
    package_1 = Package(valid_package_data())
    package_2 = Package(valid_package_data_with_different_name())

    assert package_1 > package_2
    assert package_2 < package_1
    assert package_1 != package_2


def test_should_be_compareable_by_version_if_names_are_equal():
    package_1 = Package(valid_package_data())
    package_2 = Package(valid_package_data_with_greater_version())

    assert package_1 < package_2
    assert package_2 > package_1
    assert package_1 != package_2


def test_package_with_provides_field_should_have_virtual_package_provides_list():
    expected = ["python3-profiler", "python3-supported-max", "python3-supported-min"]

    package = Package(valid_package_data_with_provides_field())

    provides_names = [pack.name for pack in package.provides]
    assert all(pack in provides_names for pack in expected)


def test_package_without_provides_field_should_have_empty_provides_list():
    package = Package(valid_package_data())

    assert len(package.provides) == 0


def test_package_should_return_to_original_string():
    data = valid_package_data()

    package = Package(data)

    assert str(package) == data


def valid_package_data():
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
Filename: ./python3_3.11.4-5+b1_amd64.deb"""


def valid_package_data_with_provides_field():
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
Filename: ./python3_3.11.4-5+b1_amd64.deb"""


def valid_package_data_with_greater_version():
    return valid_package_data().replace("Version: 3.11.4-5+b1", "Version: 4.11.4-5+b1")


def valid_package_data_with_different_name():
    return valid_package_data().replace("Package: python3", "Package: ca-certificates")


def valid_package_data_with_priority_field():
    return valid_package_data() + "\nPriority: required"
