import os.path

from src.packages import *
from src.update import generate_index_dictionary, add_apt_source_field


def test_get_package_dependencies_without_recommended():
    expected = ['gcc-10-base', 'libc6', 'libcrypt1', 'libgcc-s1']

    with open(os.path.join('tests', 'resources', 'libc6_packages.txt'), 'r', encoding='utf-8') as index_file:
        index_data = index_file.read()

    index = generate_index_dictionary(index_data)
    result = get_package_dependencies('libc6', index, with_recommended=False)

    assert len(result) == 4
    assert all([pack in result for pack in expected])


