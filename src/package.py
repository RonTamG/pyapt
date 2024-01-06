import re

from src.version import Version


def _into_virtual_package(self, name, package_data):
    name, *_ = name.split(" ")  # ignoring the version of the virtual package
    package_data = package_data.replace(f"Package: {self.name}", f"Package: {name}")

    return Package(package_data)


class Package:
    def __init__(self, package_data) -> None:
        matches = re.finditer(
            r"^(?P<name>\S+?):(?P<value>(.*)(\n\s.+)?)\n?", package_data, re.MULTILINE
        )
        groups = [(match.group("name"), match.group("value")) for match in matches]
        values = {name: value.replace("\n", "").strip() for (name, value) in groups}

        self.name = values["Package"]
        self.version = Version(values["Version"])
        self.architecture = values["Architecture"]
        self.maintainer = values["Maintainer"]
        self.description = values["Description"]
        self.apt_source = None

        if "Provides" in values:
            package_data = package_data.replace(f"Provides: {values['Provides']}\n", "")
            provides_list = [value.strip() for value in values["Provides"].split(",")]
            self.provides = [
                _into_virtual_package(self, name, package_data)
                for name in provides_list
            ]
        else:
            self.provides = []

    def __equ__(self, other) -> bool:
        if isinstance(other, Package):
            if self.name == other.name:
                return self.version == other.version
            else:
                return True
        else:
            raise NotImplementedError

    def __gt__(self, other) -> bool:
        if isinstance(other, Package):
            if self.name == other.name:
                return self.version > other.version
            else:
                return self.name > other.name
        else:
            raise NotImplementedError

    def __lt__(self, other) -> bool:
        if isinstance(other, Package):
            if self.name == other.name:
                return self.version < other.version
            else:
                return self.name < other.name
        else:
            raise NotImplementedError
