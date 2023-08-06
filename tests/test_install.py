from src.install import create_install_script


def test_create_install_script():
    expected = """\
#!/bin/bash

# make sure /etc/apt/sources.list exists
touch /etc/apt/sources.list

# set local repo
echo deb [trusted=yes] file:`pwd`/packages/ ./ | cat - /etc/apt/sources.list > temp && mv temp /etc/apt/sources.list

# update apt sources
apt update

# install packages
apt install libc6

# cleanup and restore original lists
tail -n +2 /etc/apt/sources.list > /etc/apt/sources.list
"""  # noqa: E501

    result = create_install_script("libc6")

    assert result == expected
