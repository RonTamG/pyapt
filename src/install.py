def create_install_script(name):
    """
    create a bash script that installs the package with all it's dependencies
    """
    script = f"""\
#!/bin/bash

if [ "$1" == "-y" ]; then
    auto_install="-y"
else
    auto_install=""
fi

# get current working directory and escape spaces
cwd=`pwd`
cwd=${{cwd// /%20}}

# set local repo
echo deb [trusted=yes] file:"${{cwd}}/packages/" ./ > /etc/apt/sources.list.d/pyapt.list

# update apt sources
apt-get update -o Dir::Etc::sourcelist="sources.list.d/pyapt.list" \\
    -o Dir::Etc::sourceparts="-" -o APT::Get::List-Cleanup="0"    

# install packages
apt install {name} $auto_install

# cleanup
rm /etc/apt/sources.list.d/pyapt.list
"""

    return script
