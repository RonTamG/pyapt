def create_install_script(name):
    """
    create a bash script that installs the package with all it's dependencies
    """
    script = f"""\
#!/bin/bash

# make sure /etc/apt/sources.list exists
touch /etc/apt/sources.list

# set local repo
echo deb [trusted=yes] file:`pwd`/packages/ ./ | cat - /etc/apt/sources.list > temp && mv temp /etc/apt/sources.list

# update apt sources
apt update

# install packages
apt install {name}

# cleanup and restore original lists
tail -n +2 /etc/apt/sources.list > /etc/apt/sources.list
"""  # noqa: E501

    return script
