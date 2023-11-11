#!/bin/bash
# This test will download and install git using pyapt.

# remove git so we can install it later
apt-get remove git -y && apt-get autoremove -y

# download the package, it will create a file called git.tar.gz
python main.py --sources-list /etc/apt/sources.list git 

# extract the contents of the file
tar -xvf git.tar.gz

# run the install script
cd temp_apt

./install.sh -y

git --version
