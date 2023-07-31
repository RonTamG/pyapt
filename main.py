import argparse
import lzma
import os
import shutil
import sys
import tarfile
import urllib.request
from glob import glob
from pathlib import Path

from src.install import create_install_script
from src.packages import get_package_dependencies, get_package_url
from src.update import (
    add_apt_source_field,
    add_virtual_indexes,
    dpkg_version_compare,
    generate_index_dictionary,
    get_apt_sources,
    get_index_urls,
    get_release_urls,
    parse_sources_list,
    url_into_saved_file_name,
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


def is_downloaded(filename, directory):
    """
    check if file is in directory
    """
    return glob(os.path.join(directory, "**", filename)) != []


def get(url):
    """
    send a get request to the specified url and return the response
    """
    with urllib.request.urlopen(url) as response:
        if response.status == 200:
            return response.read()
        else:
            return ""


def tar_dir(path, name):
    with tarfile.open(name, "w:gz") as tar:
        for root, dirs, files in os.walk(path):
            for f in files:
                tar.add(os.path.join(root, f))


def save_update_file(name, data, temp_folder):
    """
    save a file to a subdirectory 'update' in the temp directory
    """
    # create directory if it doesn't exist
    update_directory = os.path.join(temp_folder, "update")
    Path(update_directory).mkdir(parents=True, exist_ok=True)

    path = os.path.join(update_directory, name)
    with open(path, "wb") as update_file:
        update_file.write(data)

    return path


def save_package_file(name, data, temp_folder):
    """
    save a file to a subdirectory 'packages' in the temp directory
    """
    # create directory if it doesn't exist
    update_directory = os.path.join(temp_folder, "packages")
    Path(update_directory).mkdir(parents=True, exist_ok=True)

    path = os.path.join(update_directory, name)
    with open(path, "wb") as update_file:
        update_file.write(data)

    return name


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
    with open(sources_list_path, "r") as sources_list:
        data = sources_list.read()

    # generate urls from sources list
    parts = parse_sources_list(data)
    urls = get_release_urls(parts)
    urls.extend(get_index_urls(parts, architecture=DEFAULT_ARCHITECTURE))

    # download index files and save them
    url_filenames = [(url, url_into_saved_file_name(url)) for url in urls]
    url_filenames_to_download = [
        (url, name)
        for url, name in url_filenames
        if not is_downloaded(name, temp_folder)
    ]
    if len(url_filenames_to_download) == 0:
        _, names = zip(*url_filenames)
        saved = (os.path.join(temp_folder, "update", name) for name in names)
    else:
        urls_to_download, filenames = zip(*url_filenames_to_download)
        downloads = (get(url) for url in urls_to_download)
        saved = (
            save_update_file(name, data, temp_folder)
            for name, data in zip(filenames, downloads)
        )
        saved = progressbar(saved, len(urls_to_download), prefix="Update: ")

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

    url_filenames = [(url, os.path.basename(url)) for url in urls]
    url_filenames_to_download = [
        (url, name)
        for url, name in url_filenames
        if not is_downloaded(name, temp_folder)
    ]
    if len(url_filenames_to_download) == 0:
        _, names = zip(*url_filenames)
        saved = names
    else:
        urls_to_download, filenames = zip(*url_filenames_to_download)
        downloads = (get(url) for url in urls_to_download)
        saved = (
            save_package_file(name, data, temp_folder)
            for name, data in zip(filenames, downloads)
        )
        saved = progressbar(saved, len(urls_to_download), prefix=f"{name}: ")

    return list(saved)


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
        filenames = download_package(
            name,
            index,
            temp_folder,
            with_dependencies,
            with_recommended,
            with_pre_dependencies,
            with_required,
        )
        write_install_script(filenames, temp_folder)
        tar_dir(temp_folder, f"{name}.tar.gz")

        if not args.keep:
            shutil.rmtree(os.path.join(temp_folder, "packages"))
            os.remove(os.path.join(temp_folder, "install.sh"))
    if not (args.keep or args.keep_update):
        shutil.rmtree(temp_folder)


if __name__ == "__main__":
    main()
