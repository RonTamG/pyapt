from src.install import create_install_script


def test_install_script_generation_is_successfull():
    expected = """\
#!/bin/bash

# set local repo
echo deb [trusted=yes] file:`pwd`/packages/ ./ > /etc/apt/sources.list.d/pyapt.list

# update apt sources
apt-get update -o Dir::Etc::sourcelist="sources.list.d/pyapt.list" \\
    -o Dir::Etc::sourceparts="-" -o APT::Get::List-Cleanup="0"    

# install packages
apt install libc6

# cleanup
rm /etc/apt/sources.list.d/pyapt.list
"""

    result = create_install_script("libc6")

    assert result == expected
