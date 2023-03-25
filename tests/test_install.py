from src.install import *


def test_create_install_script():
    filenames = ['libc6_2.31-13+deb11u5_amd64.deb',
                 'libgcc-s1_10.2.1-6_amd64.deb',
                 'libcrypt1_4.4.18-4_amd64.deb',
                 'gcc-10-base_10.2.1-6_amd64.deb'
                 ]

    expected = '''\
#!/bin/bash

cp ./update/* /var/lib/apt/lists/
dpkg --refuse-downgrade -i ./packages/gcc-10-base_10.2.1-6_amd64.deb
dpkg --refuse-downgrade -i ./packages/libcrypt1_4.4.18-4_amd64.deb
dpkg --refuse-downgrade -i ./packages/libgcc-s1_10.2.1-6_amd64.deb
dpkg --refuse-downgrade -i ./packages/libc6_2.31-13+deb11u5_amd64.deb
apt --fix-broken install --no-download -y\
'''

    result = create_install_script(filenames)

    assert result == expected
