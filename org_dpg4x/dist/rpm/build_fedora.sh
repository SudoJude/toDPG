#!/bin/sh
# Script to create an rpm from a git checkout

cd $(dirname $0)/../..
python setup.py sdist --formats=bztar
cp dist/dpg4x-*.tar.bz2 ~/rpmbuild/SOURCES/
rpmbuild -ba dist/rpm/dpg4x.spec 
