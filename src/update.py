import logging
import re


def generate_index_dictionary(index_data):
    """
    create a dictionary of the package index from an index file's data

    original file usually named Packages.xz
    """
    index = {}
    for data in index_data.strip().split("\n\n"):
        values = {}
        name = ""
        for line in data.splitlines():
            if line.startswith(" ") and name in values:
                values[name] += line
            else:
                try:
                    name, value = line.split(": ", maxsplit=1)
                except ValueError:
                    logging.warning(
                        f'failed to parse: "{line}" in package data:\n{data}'
                    )
                    continue

                values[name] = value

        try:
            if values["Package"] not in index:
                index[values["Package"]] = values
            else:
                # add to the index if the version is a higher version than the previous
                new_version = values["Version"]
                current_version = index[values["Package"]]["Version"]
                if debian_upstream_compare(new_version, current_version) > 0:
                    index[values["Package"]] = values
        except KeyError:
            logging.warning(f'failed to parse: "{data}" as package')

    return index


def get_apt_sources(url):
    """
    return the apt sources of a given index package url
    """
    pattern = re.compile(
        r"(?P<url>\w+://.+?/.+)/dists/(?P<dist>.+?)/(?P<component>.+?)/binary-(?P<arch>.+?)/Packages.xz"
    )
    result = re.match(pattern, url)
    if result is None:
        raise ValueError("url has invalid format")

    uri, dist, component, architecture = result.groups()

    return f"{uri} {dist}/{component} {architecture}"


def get_index_name(index):
    """
    returns the name of the index without any version or architecture infromation
    """
    # remove version
    name = index.split()[0].strip()
    # remove architecture
    if ":" in name:
        (name, architecture) = name.split(":")
        if architecture != "any":
            logging.warning(
                f"error processing package {name}: no support for architecture {architecture}"  # noqa: E501
            )

    return name


def get_provides_list(index):
    """
    this list includes the names of virtual packages that point to this one
    """
    if "Provides" in index:
        return index["Provides"].split(",")
    else:
        return []


def add_virtual_indexes(index):
    """
    add virtual packages to an index

    modifies the given index.
    """
    virtual_packages = {}

    for values in index.values():
        provides = get_provides_list(values)
        if "Provides" in values:
            del values["Provides"]
        for virtual_index in provides:
            virtual_packages[get_index_name(virtual_index)] = values

    index.update(virtual_packages)

    return index


def add_apt_source_field(package_index, source):
    """
    add the Apt-Source field to every package in the given package index
    """
    for package in package_index.values():
        package["Apt-Source"] = source

    return package_index


def split_debian_version(version):
    """
    split a debian version string into an epoch, upstream version and debian revision
    """
    pattern = re.compile(
        r"((\d+):)?(([0-9A-Za-z.+~-]+(?=-))|([0-9A-Za-z.+~]+))(-([0-9A-Za-z.+~]+))?"
    )
    result = re.match(pattern, version)

    if result is None:
        raise AssertionError(
            f'function failed to match "{version}" as a dpkg version string'
        )
    if result.string != version:
        raise AssertionError(
            f"function matched {result.string} instead of {version} when must match all input string"  # noqa: E501
        )

    _, epoch, upstream, _, _, _, revision = result.groups("0")

    return epoch, upstream, revision


def order(c):
    """
    give a weight to the character to order in the debian version comparison.
    """
    if c.isdigit():
        return 0
    elif c.isalpha():
        return ord(c)
    elif c == "~":
        return -1
    elif c == " ":
        return 0
    elif c:
        return ord(c) + 256
    else:
        return 0


def debian_upstream_compare(first, second):
    """
    compare a debian upstream version or revision string with another
    """
    first = first.ljust(len(second), " ")
    second = second.ljust(len(first), " ")

    for a, b in zip(first, second):
        if not a.isdigit() or not b.isdigit():
            ac = order(a)
            bc = order(b)
            if ac != bc:
                return ac - bc

        if a.isdigit() and b.isdigit():
            diff = int(a) - int(b)
            if diff != 0:
                return diff
    else:
        return 0


def dpkg_version_compare(a, b):
    """
    compare 2 debain version strings
    """
    a_epoch, a_version, a_revision = split_debian_version(a)
    b_epoch, b_version, b_revision = split_debian_version(b)

    if int(a_epoch) > int(b_epoch):
        return 1
    if int(a_epoch) < int(b_epoch):
        return -1

    rc = debian_upstream_compare(a_version, b_version)
    if rc:
        return rc

    return debian_upstream_compare(a_revision, b_revision)


def index_to_package_file_format(package):
    return "\n".join([f"{key}: {value}" for key, value in package.items()])
