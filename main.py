import argparse
import lzma
import os
import re
import shutil
import sys
import tarfile
from pathlib import Path

from src.file_manager import FileManager
from src.install import create_install_script
from src.packages import get_package_dependencies, get_package_url
from src.sources_list import SourcesList
from src.update import (
    add_apt_source_field,
    add_virtual_indexes,
    dpkg_version_compare,
    generate_index_dictionary,
    get_apt_sources,
    index_to_package_file_format,
)

DEFAULT_ARCHITECTURE = "amd64"
CLEAR = "\x1b[0J"
SAVE = "\x1b7"
RESTORE = "\x1b8"


def progressbar(it, count, prefix="", size=60, out=sys.stdout):  # Python3.6+
    """
    displays a progress bar for an iterator

    modified from the following answer:
    1. to work with generators without listing them
    2. to provide the value of the last item as a postfix.
    3. to clear the screen using ansi escape characters to fix overflowing output

    https://stackoverflow.com/a/34482761
    """

    def show(current, item=""):
        print(RESTORE, end="", file=out, flush=True)
        print(CLEAR, end="", file=out, flush=True)
        print(SAVE, end="", file=out, flush=True)

        filled = int(size * current / count)
        line = f"{prefix}[{'#' * filled}{('.' * (size - filled))}] {current}/{count} [{item}]"  # noqa: E501
        print(line, end="", file=out, flush=True)
        return len(line)

    print(SAVE, end="", file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        show(i + 1, str(item))
        yield item

    print("\n", flush=True, file=out)


def tar_dir(path, name):
    def set_permissions(tarinfo):
        tarinfo.mode = 0o655
        return tarinfo

    with tarfile.open(name, "w:gz") as tar:
        tar.add(Path(path, "packages"))
        tar.add(Path(path, "install.sh"), filter=set_permissions)


def read_lzma(path):
    """
    read a file from disk and decompress it using lzma
    """
    with open(path, "rb") as index_file:
        data = index_file.read()

    return lzma.decompress(data).decode("utf-8")


def apt_update(sources_list_path, temp_folder):
    """
    retrieve the required files and create an index of the packages
    """
    data = Path(sources_list_path).read_text()

    # generate urls from sources list
    sources_list = SourcesList(data)
    urls = sources_list.index_urls(architecture=DEFAULT_ARCHITECTURE)

    # download index files and save them
    manager = FileManager(temp_folder)
    get_urls = (manager.get_update_file(url) for url in urls)
    saved = [
        name
        for name in progressbar(get_urls, len(urls), prefix="Update: ")
        if name != ""
    ]

    # create an index dictionary from the index files
    index_files = (path for path in saved if path.endswith("Packages.xz"))
    decompressed = (read_lzma(path) for path in index_files)
    indexes = (generate_index_dictionary(data) for data in decompressed)

    # add an 'Apt-Source' key to all packages in the index, used later in order to download package  # noqa: E501
    sources = (get_apt_sources(url) for url in urls if url.endswith("Packages.xz"))
    indexes = (
        add_apt_source_field(index, source) for index, source in zip(indexes, sources)
    )

    # combine all indexes into one and add virtual packages
    full_index = {}
    for index in indexes:
        for key, value in index.items():
            if key not in full_index:
                full_index[key] = value
            elif dpkg_version_compare(full_index[key]["Version"], value["Version"]) < 0:
                full_index[key] = value
    full_index = add_virtual_indexes(full_index)

    return full_index


def download_package(
    name,
    index,
    temp_folder,
    with_dependencies=True,
    with_recommended=True,
    with_pre_dependencies=True,
    with_required=False,
):
    """
    download a package with all it's dependencies
    """
    packages = get_package_dependencies(
        name,
        index,
        with_dependencies,
        with_recommended,
        with_pre_dependencies,
        with_required,
    )

    urls = [get_package_url(name, index) for name in packages]

    # download index files and save them
    manager = FileManager(temp_folder)
    get_urls = (manager.get_package_file(url) for url in urls)
    saved = [
        name
        for name in progressbar(get_urls, len(urls), prefix=f"{name}: ")
        if name != ""
    ]

    return (saved, packages)


def write_install_script(filenames, temp_folder):
    data = create_install_script(filenames)
    with open(f"{temp_folder}/install.sh", "w", newline="\n") as install:
        install.write(data)


def create_parser():
    parser = argparse.ArgumentParser(
        prog="pyapt",
        description="A basic python implementation of apt which allows downloading packages with all dependencies on non Linux machines",  # noqa: E501
    )
    parser.add_argument("packages", nargs="+", help="list of packages to download")
    parser.add_argument(
        "--sources-list",
        default="./sources.list",
        help="the sources list to use in order to download the packages",
    )
    parser.add_argument(
        "--temp-folder",
        default="temp_apt",
        help="the folder to download update index and packages into",
    )
    parser.add_argument(
        "--keep",
        action="store_true",
        help="don't remove temp directory at the end of all package downloads",
    )
    parser.add_argument(
        "--keep-update",
        action="store_true",
        help="don't remove temp update directory at the end of all package downloads",
    )
    parser.add_argument(
        "--no-recommended",
        action="store_true",
        help="don't download recommended packages",
    )
    parser.add_argument(
        "--no-dependencies",
        action="store_true",
        help="don't download dependency packages",
    )
    parser.add_argument(
        "--no-pre-dependencies",
        action="store_true",
        help="don't download pre-dependency packages",
    )
    parser.add_argument(
        "--with-required",
        action="store_true",
        help="do download packages with priority required",
    )

    return parser


def generate_packages_file(index, packages, temp_folder):
    data = "\n\n".join(
        [index_to_package_file_format(index[package]) for package in packages]
    )
    data += "\n"
    data = re.sub(r"Filename: (.+\/)+(.+)", r"Filename: ./\2", data)

    Path(temp_folder, "packages", "Packages").write_text(data)


def main():
    args = create_parser().parse_args()
    temp_folder = args.temp_folder
    sources_list = args.sources_list
    with_recommended = not args.no_recommended
    with_dependencies = not args.no_dependencies
    with_pre_dependencies = not args.no_pre_dependencies
    with_required = args.with_required

    index = apt_update(sources_list, temp_folder)

    for name in args.packages:
        _, packages = download_package(
            name,
            index,
            temp_folder,
            with_dependencies,
            with_recommended,
            with_pre_dependencies,
            with_required,
        )
        generate_packages_file(index, packages, temp_folder)
        write_install_script(name, temp_folder)
        tar_dir(temp_folder, f"{name}.tar.gz")

        if not args.keep:
            shutil.rmtree(os.path.join(temp_folder, "packages"))
            os.remove(os.path.join(temp_folder, "install.sh"))
    if not (args.keep or args.keep_update):
        shutil.rmtree(temp_folder)


if __name__ == "__main__":
    main()
