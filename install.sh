#!/bin/bash

# This script installs the dependencies necessary for our project

# This function is called when a failure is encountered
fail()
{
    echo "Error [line $2]: '$1' could not be successfully installed" >&2
    exit 2
}


install_pip()
{
    os=`uname -s`
    if [ "$os" == "Linux" ]; then
        # assume Debian-based
        apt-get install python-pip
    elif [ "$os" == "Darwin" ]; then
        easy_install pip
    fi
}

if [[ $EUID -ne 0 ]]; then
    echo "You must be root to execute this script" >&2
    exit 1
fi

# Install pip
if [ -z "`which pip`" ]; then
    echo "Installing pip"
    install_pip()
    if [ $? != 0 ]; then
        fail pip $LINENO
    else
        echo "Pip successfully installed!" >&2
    fi
fi

# Install unirest module
echo "Installing unirest module"
pip install unirest || fail unirest $LINENO

# Install gi module
echo "Installing gi module"
pip install gi || fail gi $LINENO

# Install pyglet module
echo "Installing pyglet module"
pip install pyglet || fail pyglet $LINENO