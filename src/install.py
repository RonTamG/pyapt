def create_install_script(filenames):
    """
    create a bash script that installs the package with all it's dependencies
    """
    packages = [
        f"dpkg --refuse-downgrade -i ./packages/{name}" for name in reversed(filenames)
    ]
    install_lines = "\n".join(packages)

    script = f"""\
#!/bin/bash

# save original lists
mkdir /tmp/pyapt
mv /var/lib/apt/lists/* /tmp/pyapt/

# transfer required lists to directory
cp ./update/* /var/lib/apt/lists/

# install packages
{install_lines}

# fix installs to complete all dependencies
apt --fix-broken install --no-download -y

# cleanup and restore original lists
rm /var/lib/apt/lists/*
mv /tmp/pyapt/* /var/lib/apt/lists/
rmdir /tmp/pyapt
"""

    return script
