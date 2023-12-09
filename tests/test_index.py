# ruff: noqa: E501

from src.index import Index


def test_index_should_include_package_in_index_file():
    index_file = valid_index_file()

    index = Index(index_file)

    assert len(index) == 1


def test_should_include_all_packages_in_index_file():
    index_file = valid_index_file_with_multiple_packages()

    index = Index(index_file)

    assert len(index) == 2


def valid_index_file():
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


def valid_index_file_with_multiple_packages():
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
