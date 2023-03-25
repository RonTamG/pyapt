# pyapt

This program was made in order to solve a common issue where one wants to download an apt package with all it's dependencies on a non linux computer connected to the internet, and later install it in an offline environment.

## Why not apt-offline
The reasons I chose not to use apt-offline: 
1. It is required to be installed on both machine.
2. It requires a file to be transfered from the offline machine to the online one and then back.

I wanted a solution that requires only one file transfer, from the online machine to the offline one.

# Features

- fully cross-platform
- downloads all dependencies of a package
- single tar.gz file to move to offline machine
- generated install.sh script in the tar.gz file to allow for easy install
- prebuilt binaries for quick use on any machine
- no external dependencies or libraries required

# Usage

single package
```
pyapt git
```

multiple packages
```
pyapt git openssl
```

no recommended
```
pyapt --no-recommended git
```

include packages marked as required or important

```
pyapt --with-required git
```

keep updates between uses or keep all downloads

```
pyapt --keep-update git

pyapt --keep git
```

This program requires a sources.list file and searches for it in the current directory.

You can use `--sources-list` to specify one explicitly.

```
pyapt --sources-list ./sources git
```

# How it works
This program parses a sources.list file and uses it to resolve the package registry to use.

example sources.list
```
# deb http://snapshot.debian.org/archive/debian/20230227T000000Z bullseye main
deb http://deb.debian.org/debian bullseye main
# deb http://snapshot.debian.org/archive/debian-security/20230227T000000Z bullseye-security main
deb http://deb.debian.org/debian-security bullseye-security main
# deb http://snapshot.debian.org/archive/debian/20230227T000000Z bullseye-updates main
deb http://deb.debian.org/debian bullseye-updates main
```

After finding a registry it gets it's index files and builds a full index in the form of an in-memory dictionary.
The following files will be downloaded using the example list:
```
http://deb.debian.org/debian/dists/bullseye/InRelease
http://deb.debian.org/debian-security/dists/bullseye-security/InRelease  
http://deb.debian.org/debian/dists/bullseye-updates/InRelease
http://deb.debian.org/debian/dists/bullseye/main/binary-amd64/Packages.xz 
http://deb.debian.org/debian/dists/bullseye/main/binary-all/Packages.xz
http://deb.debian.org/debian-security/dists/bullseye-security/main/binary-amd64/Packages.xz 
http://deb.debian.org/debian-security/dists/bullseye-security/main/binary-all/Packages.xz 
http://deb.debian.org/debian/dists/bullseye-updates/main/binary-amd64/Packages.xz
http://deb.debian.org/debian/dists/bullseye-updates/main/binary-all/Packages.xz
```

Using this dictionary it can find all the dependencies of a requested package and download them from the registry.

The files above are used again during the installation process and are a part of the generated tar.gz. During the installation process these files are copied to `/var/lib/apt/lists` to be used by apt in order to finish the installation of all packages. 

These files are not cleared by default during installation and can be cleared using `rm /var/lib/apt/lists/*` after the installation finished, be carefull if you have any files you want to keep in this directory.
