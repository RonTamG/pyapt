from src.package import Package


class Index:
    def __init__(self, index_file) -> None:
        package = Package(index_file)
        self.packages = {package.name: package}

    def __len__(self) -> int:
        return len(self.packages)
