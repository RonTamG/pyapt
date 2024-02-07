import posixpath
import re

from src.version import Version


def _into_virtual_package(self, name, package_data):
    pattern = re.compile(r"(?P<name>\S+)(?: \(= (?P<version>\S+)\))?")
    result = re.match(pattern, name)
    if result is None:
        raise AssertionError(f'failed to match "{name}" as virtual package name')

    name, version = result.groups()

    package_data = package_data.replace(f"Package: {self.name}", f"Package: {name}")
    if version is not None:
        package_data = package_data.replace(
            f"Version: {self.version}", f"Version: {version}"
        )

    return Package(package_data)


def _add_list_value(list_name, values, default=list([])):
    if list_name in values:
        return [pack.strip() for pack in values[list_name].split(",")]
    else:
        return default


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

        self.pre_dependencies = _add_list_value("Pre-Depends", values)
        self.dependencies = _add_list_value("Depends", values)
        self.recommended = _add_list_value("Recommends", values)
        self.priority = values.get("Priority", "optional")

        if "Provides" in values:
            package_data = package_data.replace(f"Provides: {values['Provides']}\n", "")
            provides_list = [value.strip() for value in values["Provides"].split(",")]
            self.provides = [
                _into_virtual_package(self, name, package_data)
                for name in provides_list
            ]
        else:
            self.provides = []

        self.apt_source = ""
        self.all_fields = values

    @property
    def download_url(self):
        uri, *_ = self.apt_source.split()
        return posixpath.join(uri, self.all_fields["Filename"])

    def __repr__(self) -> str:
        return f"{self.name} ({self.version})"

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

    def __str__(self) -> str:
        return "\n".join([f"{key}: {value}" for key, value in self.all_fields.items()])
