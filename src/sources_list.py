import posixpath


def _parse_sources_list(sources_list):
    """
    parse apt sources list into parts.
    the list is found in /etc/apt/sources.list in debian distros
    """
    # remove comments
    data = filter(
        lambda line: not (line.startswith("#") or line == "\n"),
        sources_list.strip().splitlines(),
    )

    # split into parts
    parts = [line.strip().split() for line in data]

    return parts


class SourcesList:
    """
    class representing an apt sources.list file
    has methods for getting urls for release and package files
    """

    def __init__(self, sources_list):
        self.parts = _parse_sources_list(sources_list)

    def release_urls(self):
        """
        generate the list of InRelease files to fetch from the repository
        """
        return [
            posixpath.join(url, "dists", dist, "InRelease")
            for (_, url, dist, *components) in self.parts
        ]

    def index_urls(self, architecture):
        """
        generate the list of Package files to fetch from the repository
        """
        indexes = []
        for _, url, dist, *components in self.parts:
            indexes.extend(
                [
                    posixpath.join(
                        url,
                        "dists",
                        dist,
                        component,
                        "binary-" + architecture,
                        "Packages.xz",
                    )
                    for component in components
                ]
            )
        return indexes
