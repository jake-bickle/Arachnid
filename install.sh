#!/usr/bin/env bash

pkg_mngr="$( command -v yum || command -v apt-get || command -v brew)"
if test -z "$pkg_mngr" 
then
    echo "Unable to locate package manager. Please visit https://github.com/jake-bickle/Arachnid/blob/master/README.md for more information on installing manually."
    exit 1
fi

# Install dependancies
$pkg_mngr install build-essential checkinstall
$pkg_mngr install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

# Install python 3.7
cd /usr/src
wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz
tar xzf Python-3.7.4.tgz
cd Python-3.7.4
./configure
make altinstall
