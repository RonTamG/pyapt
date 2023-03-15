import posixpath
import logging
import re


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
    return [posixpath.join(url, 'dists', dist, 'InRelease') for (_, url, dist, *components) in parts]


def get_index_urls(parts, architecture):
    '''
    generate the list of Package files to fetch from the repository
    '''
    indexes = []
    for (_, url, dist, *components) in parts:
        indexes.extend([posixpath.join(url, 'dists', dist, component, 'binary-' +
                       architecture, 'Packages.xz') for component in components])
    return indexes


def url_into_saved_file_name(url):
    '''
    the files from an apt update get saved to /var/lib/apt/lists.
    the names of the files are derived from the urls used to retrieve them.
    '''
    return url.replace('http://', '').replace('/', '_')


def generate_index_dictionary(index_data):
    '''
    create a dictionary of the package index from an index file's data

    original file usually named Packages.xz
    '''
    index = {}
    for data in index_data.strip().split('\n\n'):
        values = {}
        name = ''
        for line in data.splitlines():
            if line.startswith(' ') and name in values:
                values[name] += line
            else:
                try:
                    name, value = line.split(': ', maxsplit=1)
                except ValueError:
                    logging.warning(
                        f'failed to parse: "{line}" in package data:\n{data}')

                name = name.replace('-', '_').strip()
                values[name] = value

        try:
            index[values['Package']] = values
        except KeyError:
            logging.warning(f'failed to parse: "{data}" as package')

    return index


def get_apt_sources(url):
    '''
    return the apt sources of a given index package url
    '''
    pattern = re.compile(
        '(?P<url>\w+:\/\/.+?\/.+)\/dists\/(?P<dist>.+?)\/(?P<component>.+?)\/binary-(?P<arch>.+?)\/Packages.xz')
    result = re.match(pattern, url)

    uri, dist, component, architecture = result.groups()

    return f'{uri} {dist}/{component} {architecture}'


def get_index_name(index):
    '''
    returns the name of the index without any version or architecture infromation
    '''
    # remove version
    name = index.split()[0].strip()
    # remove architecture
    if ':' in name:
        (name, architecture) = name.split(':')
        if architecture != 'any':
            logging.warning(
                f'error processing package {name}: no support for architecture {architecture}')

    return name


def get_provides_list(index):
    '''
    this list includes the names of virtual packages that point to this one
    '''
    if 'Provides' in index:
        return index['Provides'].split(',')
    else:
        return []


def add_virtual_indexes(index):
    '''
    add virtual packages to an index

    modifies the given index.
    '''
    virtual_packages = {}

    for values in index.values():
        provides = get_provides_list(values)
        if 'Provides' in values:
            del values['Provides']
        for virtual_index in provides:
            virtual_packages[get_index_name(virtual_index)] = values

    index.update(virtual_packages)

    return index


def add_apt_source_field(package_index, source):
    '''
    add the Apt-Source field to every package in the given package index
    '''
    for package in package_index.values():
        package['Apt-Source'] = source

    return package_index
