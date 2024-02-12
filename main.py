import argparse
import pickle
import re
import shutil
import tarfile
from functools import reduce
from pathlib import Path

from src.file_manager import FileManager
from src.index import Index
from src.install import create_install_script
from src.progress_bar import progressbar
from src.sources_list import SourcesList

DEFAULT_ARCHITECTURE = "amd64"


def get_apt_sources(url):
    """
    return the apt sources of a given index package url
    """
    pattern = re.compile(
        r"(?P<url>\w+://.+?/.+)/dists/(?P<dist>.+?)/(?P<component>.+?)/binary-(?P<arch>.+?)/Packages"
    )
    result = re.match(pattern, url)
    if result is None:
        raise ValueError("url has invalid format")

    uri, dist, component, architecture = result.groups()

    return f"{uri} {dist}/{component} {architecture}"


def tar_dir(path, name):
    def set_permissions(tarinfo):
        tarinfo.mode = 0o755
        return tarinfo

    with tarfile.open(name + ".tar.gz", "w:gz") as tar:
        tar.add(Path(path, "packages"), Path(name, "packages"))
        tar.add(
            Path(path, "install.sh"), Path(name, "install.sh"), filter=set_permissions
        )


def apt_update(sources_list_path, enable_progress_bar=True):
    """
    retrieve the required files and create an index of the packages
    """
    data = Path(sources_list_path).read_text()

    # generate urls from sources list
    sources_list = SourcesList(data)
    urls = sources_list.index_urls(architecture=DEFAULT_ARCHITECTURE)

    # download index files and save them
    manager = FileManager()
    index_files = (manager.get_package_index_file(url) for url in urls)
    if enable_progress_bar:
        index_files = progressbar(
            index_files, len(urls), prefix="Update: ", with_item=False
        )

    # create an index dictionary from the index files
    indexes = (Index(data) for data in index_files if len(data) > 0)

    # add an 'Apt-Source' key to all packages in the index, used later in order to download package  # noqa: E501
    sources = (get_apt_sources(url) for url in urls)
    indexes = (
        index.set_packages_apt_source(source) for index, source in zip(indexes, sources)
    )

    # combine all indexes into one and add virtual packages
    full_index = reduce(Index.combine, indexes)

    return full_index


def download_package(
    name,
    index,
    temp_folder,
    with_recommended=True,
    with_required=False,
    enable_progress_bar=True,
):
    """
    download a package with all it's dependencies
    """
    packages = index.get_package_dependencies(name, with_recommended=with_recommended)
    urls = [package.download_url for package in packages]

    # download index files and save them
    manager = FileManager()
    get_urls = (
        manager.get_package_file(url, Path(temp_folder, "packages")) for url in urls
    )

    if enable_progress_bar:
        get_urls = progressbar(get_urls, len(urls), prefix=f"{name}: ")
    [name for name in get_urls if name != ""]

    return packages


def write_install_script(name, temp_folder):
    data = create_install_script(name)
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
        "--no-recommended",
        action="store_true",
        help="don't download recommended packages",
    )
    parser.add_argument(
        "--with-required",
        action="store_true",
        help="do download packages with priority required",
    )
    parser.add_argument(
        "--no-progress-bar",
        action="store_true",
        help="remove progress bar",
    )

    return parser


def generate_packages_index_file(packages, temp_folder):
    data = "\n\n".join([str(package) for package in packages])
    data += "\n"
    data = re.sub(r"Filename: (.+\/)+(.+)", r"Filename: ./\2", data)

    Path(temp_folder, "packages", "Packages").write_text(data, encoding="utf-8")


def main():
    parser = create_parser()
    args = parser.parse_args()
    temp_folder = args.temp_folder
    sources_list = args.sources_list
    with_recommended = not args.no_recommended
    with_required = args.with_required
    enable_progress_bar = not args.no_progress_bar

    if not Path(sources_list).exists():
        parser.print_usage()
        print(f"pyapt: error: the file {sources_list} is missing")
        exit()

    index_dump_path = Path(temp_folder, "index_dump")
    if index_dump_path.exists():
        index = pickle.loads(index_dump_path.read_bytes())
    else:
        index = apt_update(sources_list, enable_progress_bar)

    for name in args.packages:
        packages = download_package(
            name,
            index,
            temp_folder,
            with_recommended,
            with_required,
            enable_progress_bar,
        )
        generate_packages_index_file(packages, temp_folder)
        write_install_script(name, temp_folder)
        index_dump_path.unlink(missing_ok=True)
        tar_dir(temp_folder, name)

    if not args.keep:
        shutil.rmtree(temp_folder)
    else:
        index_dump_path.parent.mkdir(parents=True, exist_ok=True)
        with index_dump_path.open("wb") as index_dump:
            pickle.dump(index, index_dump)


if __name__ == "__main__":
    main()
