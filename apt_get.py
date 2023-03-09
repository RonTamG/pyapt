import gzip
import logging
import pickle
import os
import sys
import tarfile
import shutil

import requests

SERVER = 'http://archive.ubuntu.com/ubuntu/'

SOURCES_LIST = 'sources.list'
TEMP_FOLDER_NAME = 'temp-apt'

logging.getLogger().setLevel(logging.INFO)

def write_temp_file(name, mode, data):
    with open(f'{TEMP_FOLDER_NAME}/{name}', mode) as temp:
        temp.write(data)

def write_update_file(url, mode, data):
    update_dir_name = TEMP_FOLDER_NAME + '/update/'
    if not os.path.isdir(update_dir_name):
        os.mkdir(update_dir_name)
    
    filename = 'update/' + url.replace('http://', '').replace('/', '_')
    write_temp_file(filename, mode, data)

def get_packages_dictionary(packages_data):
    packages = {}
    for package_data in packages_data:
        values = {}
        for line in package_data.splitlines():
            try:
                name, data = line.split(': ', maxsplit=1)
            except ValueError:
                logging.warning(f'failed to parse: "{line}" in package data:\n{package_data}')
            
            name = name.replace('-', '_').strip()
            values[name] = data

        try:
            packages[values['Package']] = values
        except KeyError:
            logging.warning(f'failed to parse: "{package_data}" as package')
    
    return packages

def get_package_name(dependency):
    # remove version
    name = dependency.split()[0].strip()
    # remove architecture
    if ':' in name:
        (name, architecture) = name.split(':')
        if architecture != 'any':
            logging.warning(f'error processing package {name}: no support for architecture {architecture}')
    
    return name

def get_provides_list(package):
    if 'Provides' in package:
        return package['Provides'].split(',')
    else:
        return []

def add_virtual_packages(packages):
    virtual_packages = {}
    
    for values in packages.values():
        provides = get_provides_list(values)
        if 'Provides' in values:
            del values['Provides']
        for package in provides:
            virtual_packages[get_package_name(package)] = values
    
    packages.update(virtual_packages)

def apt_update(sources_list):
    with open(sources_list, 'r', encoding='utf-8') as sources:
        data = sources.readlines()
        
    # remove comments
    data = filter(lambda line: not (line.startswith('#') or line == '\n'), data)

    # split into components
    split_line = [line.strip().split(' ') for line in data]

    packages_list_data = []
    for (_, url, dist, *components) in split_line:
        release = f'{url}dists/{dist}/InRelease'
        release_data = requests.get(release).text
        write_update_file(release, 'w', release_data)

        packages = [f'{url}dists/{dist}/{component}/binary-amd64/Packages.gz' for component in components]

        for package in packages:
            content = requests.get(package).content
            write_update_file(package, 'wb', content)

            package_data = gzip.decompress(content)
            packages_list_data.extend(package_data.decode('utf-8').strip().split('\n\n'))
            
    packages = get_packages_dictionary(packages_list_data)
    add_virtual_packages(packages)

    return packages

def dump_packages(packages):
    with open('packages.gz', 'wb') as out:
        dump = gzip.compress(pickle.dumps(packages))
        out.write(dump)
    
def load_packages():
    with open('packages.gz', 'rb') as package_input:
        dump = gzip.decompress(package_input.read())
        packages = pickle.loads(dump)
    return packages

def extend_unique(iterator, new):
    for element in new:
        if element not in new:
            iterator.append(element)
    return iterator

def get_dependency_list(package):
    if 'Depends' in package:
        return package['Depends'].split(')')
    else:
        return []

def get_recommended_list(package):
    if 'Recommends' in package:
        return package['Recommends'].split(')')
    else:
        return []

def get_pre_dependency_list(package):
    if 'Pre_Depends' in package:
        return package['Pre_Depends'].split(')')
    else:
        return []
    
def get_package(name, packages, with_dependencies=True, with_recommended=True, with_pre_dependencies=True):
    dependencies = [name]

    for dependency in dependencies:
        name = get_package_name(dependency)

        try:
            pack = packages[name]
        except KeyError:
            logging.error(f'failed to find package {name}')
            continue
    
        if with_dependencies:
            deps = [get_package_name(dep) for dep in get_dependency_list(pack)]
            extend_unique(dependencies, deps)
        
        if with_recommended:
            recommended = [get_package_name(dep) for dep in get_recommended_list(pack)]
            extend_unique(dependencies, recommended)

        if with_dependencies:
            pre_dependencies = [get_package_name(dep) for dep in get_pre_dependency_list(pack)]
            extend_unique(dependencies, pre_dependencies)

    return dependencies    

def progress_bar(it, prefix='', size=60, out=sys.stdout):
    count = len(it)

    def show(j):
        x = int(size * j / count)
        print(f"{prefix}[{'#' * x}{'.' * (size - x)}] {j} / {count}", end='\r', file=out, flush=True)
    show(0)
    
    for i, item in enumerate(it):
        yield item
        show(i + 1)

    print("\n", flush=True, file=out)

def write_package_file(url, response):
    package_dir = TEMP_FOLDER_NAME + '/packages/'
    if not os.path.isdir(package_dir):
        os.mkdir(package_dir)
    
    with open(package_dir + os.path.basename(url), 'wb') as package_file:
        package_file.write(response.content)
    
def download_package_urls(urls):
    for url in progress_bar(urls, 'Downloading: ', size=len(urls)):
        response = requests.get(url)

        if response.status_code == 200:
            write_package_file(url, response)
    
def download_package(name, packages, server):
    to_download = get_package(name, packages)
    urls = [server + packages[package]['Filename'] for package in to_download]

    download_package_urls(urls)
    return urls

def download_size(package_name, packages):
    to_download = get_package(package_name, packages)
    size = sum(map(lambda name: int(packages[name]['Installed_Size']), to_download))
    return size

def write_install_script(urls):
    data = '#!/bin/bash\n\n'
    data += 'cp ./update/* /var/lib/apt/lists/\n'
    lines = [f'dpkg -i ./packages/{os.path.basename(url)}' for url in reversed(urls)]
    data += '\n'.join(lines)
    data += '\napt --fix-broken install -y'

    with open(f'{TEMP_FOLDER_NAME}/install.sh', 'w', newline='\n') as install:
        install.write(data)
    
def tar_dir(path, name):
    with tarfile.open(name, 'w:gz') as tar:
        for root, dirs, files in os.walk(path):
            for f in files:
                tar.add(os.path.join(root, f))

def main():
    name = 'git'

    if not os.path.isdir(TEMP_FOLDER_NAME):
        os.mkdir(TEMP_FOLDER_NAME)
    
    packages = apt_update(SOURCES_LIST)
    urls = download_package(name, packages, SERVER)
    write_install_script(urls)

    tar_dir(TEMP_FOLDER_NAME, f'{name}.tar.gz')
    logging.info(f'written file to {name}.tar.gz')

    shutil.rmtree(TEMP_FOLDER_NAME)

if __name__ == '__main__':
    main()
