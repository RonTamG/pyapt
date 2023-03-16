import os.path

from src.packages import *
from src.update import generate_index_dictionary, add_apt_source_field


def test_get_package_dependencies_without_recommended():
    expected = ['libc6', 'libcrypt1', 'libgcc-s1']

    with open(os.path.join('tests', 'resources', 'libc6_packages.txt'), 'r', encoding='utf-8') as index_file:
        index_data = index_file.read()

    index = generate_index_dictionary(index_data)
    result = get_package_dependencies('libc6', index, with_recommended=False)

    assert len(result) == 3
    assert all([pack in result for pack in expected])

def test_get_package_dependencies_without_required_priority():
    expected = ['gcc-10-base', 'libc6', 'libcrypt1', 'libgcc-s1']

    with open(os.path.join('tests', 'resources', 'libc6_packages.txt'), 'r', encoding='utf-8') as index_file:
        index_data = index_file.read()

    index = generate_index_dictionary(index_data)
    result = get_package_dependencies('libc6', index, with_recommended=False, with_required=True)

    assert len(result) == 4
    assert all([pack in result for pack in expected])



def test_get_package_url():
    expected = [
        'http://deb.debian.org/debian/pool/main/g/gcc-10/gcc-10-base_10.2.1-6_amd64.deb',
        'http://deb.debian.org/debian/pool/main/g/glibc/libc6_2.31-13+deb11u5_amd64.deb',
        'http://deb.debian.org/debian/pool/main/libx/libxcrypt/libcrypt1_4.4.18-4_amd64.deb',
        'http://deb.debian.org/debian/pool/main/g/gcc-10/libgcc-s1_10.2.1-6_amd64.deb',
    ]

    with open(os.path.join('tests', 'resources', 'libc6_packages.txt'), 'r', encoding='utf-8') as index_file:
        index_data = index_file.read()
    index = generate_index_dictionary(index_data)
    add_apt_source_field(index, 'http://deb.debian.org/debian')

    packages = ['gcc-10-base', 'libc6', 'libcrypt1', 'libgcc-s1']

    result = [get_package_url(name, index) for name in packages]

    assert result == expected
