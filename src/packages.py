import posixpath

from src.update import get_index_name


def extend_unique(iterator, new):
    """
    append items from new into iterator if they are not already in iterator
    """
    for element in new:
        if element not in iterator:
            iterator.append(element)
    return iterator


def get_dependency_list(package):
    if "Depends" in package:
        return package["Depends"].split(",")
    else:
        return []


def get_recommended_list(package):
    if "Recommends" in package:
        return package["Recommends"].split(",")
    else:
        return []


def get_pre_dependency_list(package):
    if "Pre-Depends" in package:
        return package["Pre-Depends"].split(",")
    else:
        return []


def get_package_dependencies(
    current,
    index,
    packages=None,
    with_dependencies=True,
    with_recommended=True,
    with_pre_dependencies=True,
    with_required=False,
):
    """
    return a list of all package names that are needed to install the package specified in 'name'

    by default includes all pre-dependencies, dependencies and recommended packages
    these are the defaults that 'apt install' has
    """  # noqa: E501
    current = get_index_name(current)

    if packages is None:
        packages = []

    if current not in index:
        raise KeyError(current)

    if index[current]["Priority"] in ["required", "important"] and (not with_required):
        return None

    if current in packages:
        return None
    else:
        packages.append(current)

    if with_pre_dependencies:
        try:
            [
                get_package_dependencies(
                    dep,
                    index,
                    packages,
                    with_dependencies,
                    with_recommended,
                    with_pre_dependencies,
                    with_required,
                )
                for dep in get_pre_dependency_list(index[current])
            ]
        except KeyError:
            raise KeyError(current)

    if with_dependencies:
        try:
            [
                get_package_dependencies(
                    dep,
                    index,
                    packages,
                    with_dependencies,
                    with_recommended,
                    with_pre_dependencies,
                    with_required,
                )
                for dep in get_dependency_list(index[current])
            ]
        except KeyError:
            raise KeyError(current)

    if with_recommended:
        try:
            [
                get_package_dependencies(
                    dep,
                    index,
                    packages,
                    with_dependencies,
                    with_recommended,
                    with_pre_dependencies,
                    with_required,
                )
                for dep in get_recommended_list(index[current])
            ]
        except KeyError:
            pass

    return packages


def get_package_url(name, index):
    """
    return the url to request in order to download the package
    """
    URI = 0
    package = index[name]
    return posixpath.join(package["Apt-Source"].split()[URI], package["Filename"])
