import os.path
def parse_sources_list(sources_list):
    '''
    parse apt sources list into parts.
    the list is found in /etc/apt/sources.list in debian distros
    '''
    # remove comments
    data = filter(lambda line: not (line.startswith(
        '#') or line == '\n'), sources_list.strip().splitlines())

    # split into parts
    parts = [line.strip().split() for line in data]

    return parts


def get_release_urls(parts):
    '''
    generate the list of InRelease files to fetch from the repository
    '''
    return [os.path.join(url, 'dists', dist, 'InRelease') for (_, url, dist, *components) in parts]


def get_index_urls(parts, architecture):
    '''
    generate the list of Package files to fetch from the repository
    '''
    indexes = []
    for (_, url, dist, *components) in parts:
        indexes.extend([os.path.join(url, 'dists', dist, component, 'binary-' +
                       architecture, 'Packages.xz') for component in components])
    return indexes


def url_into_saved_file_name(url):
    '''
    the files from an apt update get saved to /var/lib/apt/lists.
    the names of the files are derived from the urls used to retrieve them.
    '''
    return url.replace('http://', '').replace('/', '_')


