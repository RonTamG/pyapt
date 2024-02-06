import re
from operator import itemgetter
from typing import Dict

from src.package import Package
from src.version import Version

LATEST_INDEX = 0


class Index:
    def __init__(self, index_file: str) -> None:
        packages_data = index_file.strip().split("\n\n")
        packages = [Package(data) for data in packages_data]

        self.packages: Dict[str, Dict[Version, Package]] = {}

        [self.add_package(package) for package in packages]

    def __len__(self) -> int:
        return len(self.packages)

    def __contains__(self, key):
        return self.search(key) is not None

    def combine(self, other):
        if not isinstance(other, Index):
            raise NotImplementedError()

        for package_versions in other.packages.values():
            for package in package_versions.values():
                self.add_package(package)

        return self

    def search(self, name) -> Package | None:
        pattern = r"([^\s:]+)(?::(\S+))?(?: \((<<|<=|=|>=|>>) (\S+)\))?"
        result = None

        if (match := re.match(pattern, name)) is not None:
            # here we ignore the architecture
            package, _, operation, target_version = match.groups()

            if (package_versions := self.packages.get(package, None)) is not None:
                if operation is None:
                    result = list(package_versions.values())[LATEST_INDEX]
                elif operation == "=":
                    result = package_versions[Version(target_version)]
                else:
                    compare = {
                        ">>": Version.__gt__,
                        "<<": Version.__lt__,
                        ">=": Version.__ge__,
                        "<=": Version.__le__,
                    }[operation]

                    result = next(
                        (
                            package
                            for version, package in package_versions.items()
                            if compare(version, Version(target_version))
                        ),
                        None,
                    )

        return result

    def add_package(self, package: Package):
        if package.name in self.packages:
            versions = self.packages[package.name]
            versions[package.version] = package
            self.packages[package.name] = {
                k: v
                for k, v in sorted(versions.items(), key=itemgetter(1), reverse=True)
            }
        else:
            self.packages[package.name] = {package.version: package}

        [self.add_package(pack) for pack in package.provides]

    def set_packages_apt_source(self, source):
        for package_versions in self.packages.values():
            for package in package_versions.values():
                package.apt_source = source

        return self

    def get_package_dependencies(self, name, packages=None, with_recommended=False):
        current = self.search(name)

        if current is None:
            raise KeyError(name)

        if packages is None:
            packages = []

        if current.priority in ["required", "important"]:
            return None

        if current in packages:
            return None
        else:
            packages.append(current)

        [
            self.get_package_dependencies(dep, packages, with_recommended)
            for dep in current.pre_dependencies
        ]

        [
            self.get_package_dependencies(dep, packages, with_recommended)
            for dep in current.dependencies
        ]

        if with_recommended:
            try:
                [
                    self.get_package_dependencies(dep, packages, with_recommended)
                    for dep in current.recommended
                ]
            except KeyError:
                pass

        return packages
