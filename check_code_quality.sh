#!/usr/bin/env bash

echo "=== alpha2aleph project : code quality ==="
echo "... this script requires pep8 AND pylint."

echo "=== pep8 --max-line-length=100 alpha2aleph/ ==="
pep8 --max-line-length=100 alpha2aleph/

echo "=== pep8 --max-line-length=100 tests/ ==="
pep8 --max-line-length=100 tests/

echo "=== pylint alpha2aleph/ ==="
touch alpha2aleph/__init__.py  # required to pylint a directory
pylint alpha2aleph/
rm alpha2aleph/__init__.py

echo "=== pylint tests/ ==="
touch tests/__init__.py  # required to pylint a directory
pylint tests/
rm tests/__init__.py