import logging
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
    if "Pre_Depends" in package:
        return package["Pre_Depends"].split(",")
    else:
        return []


def get_package_dependencies(
    name,
    packages,
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
    dependencies = [name]
    i = 0
    while i < len(dependencies):
        name = get_index_name(dependencies[i])

        try:
            pack = packages[name]
        except KeyError:
            logging.error(f"failed to find package {name}")
            i += 1
            continue

        if with_dependencies:
            deps = [get_index_name(dep) for dep in get_dependency_list(pack)]
            extend_unique(dependencies, deps)

        if with_recommended:
            recommended = [get_index_name(dep) for dep in get_recommended_list(pack)]
            extend_unique(dependencies, recommended)

        if with_pre_dependencies:
            pre_dependencies = [
                get_index_name(dep) for dep in get_pre_dependency_list(pack)
            ]
            extend_unique(dependencies, pre_dependencies)

        if not with_required:
            dependencies = [
                dep
                for dep in dependencies
                if packages[dep]["Priority"] not in ["required", "important"]
            ]

        i += 1

    return dependencies


def get_package_url(name, index):
    """
    return the url to request in order to download the package
    """
    URI = 0
    package = index[name]
    return posixpath.join(package["Apt-Source"].split()[URI], package["Filename"])
