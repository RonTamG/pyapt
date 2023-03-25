def create_install_script(filenames):
    '''
    create a bash script that installs the package with all it's dependencies
    '''
    packages = [f'dpkg --refuse-downgrade -i ./packages/{name}' for name in reversed(filenames)]

    data = '#!/bin/bash\n\n'
    data += 'cp ./update/* /var/lib/apt/lists/\n'
    data += '\n'.join(packages)
    data += '\n'
    data += 'apt --fix-broken install --no-download -y'

    return data
