#!/usr/bin/env bash

# alpha2aleph project

echo "=== alpha2aleph ==="
echo "=== this a bunch of various steps to be executed before shipping a new version to Pypi ==="

#-------------------------------------------------------------------------------
echo
echo     "   = (a) remove build/"
read -p "  = go on ? ('y' to continue) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

rm -rf build/

#-------------------------------------------------------------------------------
echo
echo     "   = (a) remove dist/"
read -p "  = go on ? ('y' to continue) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

rm -rf dist/

#-------------------------------------------------------------------------------
echo
echo     "   = (b) remove every .~ file"
read -p "  = go on ? ('y' to continue) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

find . -type f -name '*~' -exec rm -f '{}' \;

# #-------------------------------------------------------------------------------
# echo
# echo     "   = (c) pimydoc"
# read -p "  = go on ? ('y' to continue) " -n 1 -r
# echo
# if [[ ! $REPLY =~ ^[Yy]$ ]]
# then
#     exit 1
# fi

# pimydoc

#-------------------------------------------------------------------------------
echo
echo    "  = (d) next step : $ python3 setup.py sdist bdist_wheel"
read -p "  = go on ? ('y' to continue) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

python3 setup.py sdist bdist_wheel

#-------------------------------------------------------------------------------
echo
echo    "  = (e) next step : $ twine upload --repository-url https://test.pypi.org/legacy/ dist/*"
read -p "  = go on ? ('y' to continue) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

twine upload --repository-url https://test.pypi.org/legacy/ dist/*

#-------------------------------------------------------------------------------
echo
echo    "  = (f) next step : $ twine upload dist/*"
read -p "  = go on ? ('y' to continue) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

twine upload dist/*

#-------------------------------------------------------------------------------
echo
echo    "  = (i) next step : $ sudo -H pip3 install alpha2aleph --upgrade"
read -p "  = go on ? ('y' to continue) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

sudo -H pip3 install alpha2aleph --upgrade --no-cache-dir

#-------------------------------------------------------------------------------
echo
echo    "  = (i) next step : $ alpha2aleph --about"
read -p "  = go on ? ('y' to continue) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

alpha2aleph --about