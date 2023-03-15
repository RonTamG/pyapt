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


