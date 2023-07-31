from src.install import create_install_script


def test_create_install_script():
    filenames = [
        "libc6_2.31-13+deb11u5_amd64.deb",
        "libgcc-s1_10.2.1-6_amd64.deb",
        "libcrypt1_4.4.18-4_amd64.deb",
        "gcc-10-base_10.2.1-6_amd64.deb",
    ]

    expected = """\
#!/bin/bash

# save original lists
mkdir /tmp/pyapt
mv /var/lib/apt/lists/* /tmp/pyapt/

# transfer required lists to directory
cp ./update/* /var/lib/apt/lists/

# install packages
dpkg --refuse-downgrade -i ./packages/gcc-10-base_10.2.1-6_amd64.deb
dpkg --refuse-downgrade -i ./packages/libcrypt1_4.4.18-4_amd64.deb
dpkg --refuse-downgrade -i ./packages/libgcc-s1_10.2.1-6_amd64.deb
dpkg --refuse-downgrade -i ./packages/libc6_2.31-13+deb11u5_amd64.deb

# fix installs to complete all dependencies
apt --fix-broken install --no-download -y

# cleanup and restore original lists
rm /var/lib/apt/lists/*
mv /tmp/pyapt/* /var/lib/apt/lists/
rmdir /tmp/pyapt
"""

    result = create_install_script(filenames)

    assert result == expected
