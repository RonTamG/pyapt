from operator import itemgetter
from typing import Dict

from src.package import Package
from src.version import Version


class Index:
    def __init__(self, index_file: str) -> None:
        packages_data = index_file.strip().split("\n\n")
        packages = [Package(data) for data in packages_data]

        self.packages: Dict[str, Dict[Version, Package]] = {}

        [self.add_package(package) for package in packages]

    def __len__(self) -> int:
        return len(self.packages)

    def search(self, name) -> Package:
        return list(self.packages[name].values())[0]

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
