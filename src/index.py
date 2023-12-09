from src.package import Package


class Index:
    def __init__(self, index_file: str) -> None:
        packages_data = index_file.strip().split("\n\n")
        packages = [Package(data) for data in packages_data]

        self.packages = {package.name: package for package in packages}

    def __len__(self) -> int:
        return len(self.packages)

    def search(self, name) -> Package:
        return self.packages[name]
