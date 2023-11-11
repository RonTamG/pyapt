from pathlib import Path

from src.packages import get_package_dependencies, get_package_url
from src.update import (
    add_apt_source_field,
    add_virtual_indexes,
    generate_index_dictionary,
)


def test_package_dependencies_collection_with_dependencies_and_recommended_is_successfull():  # noqa: E501
    index = valid_index()

    result = get_package_dependencies("python3", index)

    assert len(result) == 43


def test_package_dependencies_collection_without_recommended_packages_is_successful():
    index = valid_index()

    result = get_package_dependencies("python3", index, with_recommended=False)

    assert len(result) == 33


def test_package_dependencies_collection_with_required_packages_is_successful():
    index = valid_index()

    result = get_package_dependencies("python3", index, with_required=True)

    assert len(result) == 104


def test_package_dependencies_collection_without_pre_dependencies_is_successful():
    index = valid_index()

    result = get_package_dependencies("python3", index, with_pre_dependencies=False)

    assert len(result) == 42


def test_package_download_url_generation_is_successfull():
    source = "http://deb.debian.org/debian"
    index = valid_index_with_apt_source(source)
    expected = "http://deb.debian.org/debian/./python3_3.11.4-5+b1_amd64.deb"

    result = get_package_url("python3", index)

    assert result == expected


def valid_index():
    with open(
        Path("tests", "resources", "python_Packages"), "r", encoding="utf-8"
    ) as index_file:
        index_data = index_file.read()

    index = generate_index_dictionary(index_data)
    add_virtual_indexes(index)

    return index


def valid_index_with_apt_source(source):
    index = valid_index()
    add_apt_source_field(index, source)

    return index
