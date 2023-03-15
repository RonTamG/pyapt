import logging
import os
import shutil
import lzma
import pickle
import re
import tarfile
import argparse

import urllib.request
from pathlib import Path

from src.update import *
from src.packages import *
from src.install import *

DEFAULT_ARCHITECTURE = 'amd64'
TEMP_FOLDER_NAME = 'temp_apt'


def get(url):
    '''
    send a get request to the specified url and return the response
    '''
    with urllib.request.urlopen(url) as response:
        if response.status == 200:
            return response.read()
        else:
            return ''


def tar_dir(path, name):
    with tarfile.open(name, 'w:gz') as tar:
        for root, dirs, files in os.walk(path):
            for f in files:
                tar.add(os.path.join(root, f))


def save_update_file(name, data):
    '''
    save a file to a subdirectory 'update' in the temp directory 
    '''
    # create directory if it doesn't exist
    update_directory = os.path.join(TEMP_FOLDER_NAME, 'update')
    Path(update_directory).mkdir(parents=True, exist_ok=True)

    path = os.path.join(update_directory, name)
    with open(path, 'wb') as update_file:
        update_file.write(data)

    return path


def save_package_file(name, data):
    '''
    save a file to a subdirectory 'packages' in the temp directory 
    '''
    # create directory if it doesn't exist
    update_directory = os.path.join(TEMP_FOLDER_NAME, 'packages')
    Path(update_directory).mkdir(parents=True, exist_ok=True)

    path = os.path.join(update_directory, name)
    with open(path, 'wb') as update_file:
        update_file.write(data)

    return name


def read_lzma(path):
    '''
    read a file from disk and decompress it using lzma
    '''
    with open(path, 'rb') as index_file:
        data = index_file.read()

    return lzma.decompress(data).decode('utf-8')


def apt_update(sources_list_path):
    '''
    retrieve the required files and create an index of the packages
    '''
    with open(sources_list_path, 'r') as sources_list:
        data = sources_list.read()

    # generate urls from sources list
    parts = parse_sources_list(data)
    urls = get_release_urls(parts)
    urls.extend(get_index_urls(parts, architecture=DEFAULT_ARCHITECTURE))

    # download index files and save them
    filenames = (url_into_saved_file_name(url) for url in urls)
    downloads = (get(url) for url in urls)
    saved = (save_update_file(name, data)
             for name, data in zip(filenames, downloads))

    # create an index dictionary from the index files
    index_files = (path for path in saved if path.endswith('Packages.xz'))
    decompressed = (read_lzma(path) for path in index_files)
    indexes = (generate_index_dictionary(data) for data in decompressed)

    # add an 'Apt-Source' key to all packages in the index, used later in order to download package
    sources = (get_apt_sources(url)
               for url in urls if url.endswith('Packages.xz'))
    indexes = (add_apt_source_field(index, source)
               for index, source in zip(indexes, sources))

    # combine all indexes into one and add virtual packages
    full_index = {}
    [full_index.update(index) for index in indexes]
    full_index = add_virtual_indexes(full_index)

    return full_index


def download_package(name, index, with_dependencies=True, with_recommended=True, with_pre_dependencies=True):
    '''
    download a package with all it's dependencies
    '''
    packages = get_package_dependencies(
        name, index, with_dependencies, with_recommended, with_pre_dependencies)

    urls = [get_package_url(name, index) for name in packages]
    filenames = (os.path.basename(url) for url in urls)
    downloads = (get(url) for url in urls)
    save = (save_package_file(name, data)
            for name, data in zip(filenames, downloads))

    return list(save)


def write_install_script(filenames):
    data = create_install_script(filenames)
    with open(f'{TEMP_FOLDER_NAME}/install.sh', 'w', newline='\n') as install:
        install.write(data)

def create_parser():
    parser = argparse.ArgumentParser(
                    prog='pyapt',
                    description='A basic python implementation of apt which allows downloading packages with all dependencies on non Linux machines')
    parser.add_argument('packages', nargs='+', help='list of packages to download')

    return parser

def main():
    args = create_parser().parse_args()

    index = apt_update('sources.list')

    for name in args.packages:
        filenames = download_package(name, index)
        write_install_script(filenames)
        tar_dir(TEMP_FOLDER_NAME, f'{name}.tar.gz')
        
        shutil.rmtree(os.path.join(TEMP_FOLDER_NAME, 'packages'))
        os.remove(os.path.join(TEMP_FOLDER_NAME, 'install.sh'))




if __name__ == '__main__':
    main()
