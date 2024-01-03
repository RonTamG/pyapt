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

    def search(self, name) -> Package | None:
        result = None

        if (
            match := re.match(r"(\S+)(?: \((<<|<=|=|>=|>>) (\S+)\))?", name)
        ) is not None:
            package, operation, target_version = match.groups()

            package_versions = self.packages[package]

            match operation:
                case None:
                    result = list(package_versions.values())[LATEST_INDEX]
                case "=":
                    target_version = Version(target_version)
                    result = package_versions[target_version]
                case ">>":
                    target_version = Version(target_version)
                    result = next(
                        (
                            package
                            for version, package in package_versions.items()
                            if version > target_version
                        ),
                        None,
                    )
                case "<<":
                    target_version = Version(target_version)
                    result = next(
                        (
                            package
                            for version, package in package_versions.items()
                            if version < target_version
                        ),
                        None,
                    )
                case ">=":
                    target_version = Version(target_version)
                    result = next(
                        (
                            package
                            for version, package in package_versions.items()
                            if version >= target_version
                        )
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
