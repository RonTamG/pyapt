from src.install import create_install_script


def test_install_script_generation_is_successfull():
    expected = """\
#!/bin/bash

if [ "$1" == "-y" ]; then
    auto_install="-y"
else
    auto_install=""
fi

# get current working directory and escape spaces
cwd=`pwd`
cwd=${cwd// /%20}

# set local repo
echo deb [trusted=yes] file:"${cwd}/packages/" ./ > /etc/apt/sources.list.d/pyapt.list

# update apt sources
apt-get update -o Dir::Etc::sourcelist="sources.list.d/pyapt.list" \\
    -o Dir::Etc::sourceparts="-" -o APT::Get::List-Cleanup="0"    

# install packages
apt install libc6 $auto_install

# cleanup
rm /etc/apt/sources.list.d/pyapt.list
"""

    result = create_install_script("libc6")

    assert result == expected
