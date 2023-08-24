import posixpath


def _parse_sources_list(sources_list):
    """
    parse apt sources list into parts.
    the list is found in /etc/apt/sources.list in debian distros
    """
    # remove comments
    lines = [line.strip() for line in sources_list.splitlines()]
    lines = [line for line in lines if not (line.startswith("#") or line == "")]
    # split into parts
    parts = [line.strip().split() for line in lines]

    return parts


class SourcesList:
    """
    class representing an apt sources.list file
    has methods for getting urls for release and package files
    """

    def __init__(self, sources_list):
        self.parts = _parse_sources_list(sources_list)

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
                        "Packages",
                    )
                    for component in components
                ]
            )
        return indexes
