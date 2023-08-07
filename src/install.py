def create_install_script(name):
    """
    create a bash script that installs the package with all it's dependencies
    """
    script = f"""\
#!/bin/bash

# set local repo
echo deb [trusted=yes] file:`pwd`/packages/ ./ > /etc/apt/sources.list.d/pyapt.list

# update apt sources
apt-get update -o Dir::Etc::sourcelist="sources.list.d/pyapt.list" \\
    -o Dir::Etc::sourceparts="-" -o APT::Get::List-Cleanup="0"    

# install packages
apt install {name}

# cleanup
rm /etc/apt/sources.list.d/pyapt.list
"""

    return script
