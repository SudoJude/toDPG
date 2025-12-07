#!/bin/sh
# Script to create a deb package from a git checkout

cd $(dirname $0)/../..
debuild -i -us -uc -b
mv ../*.deb dist

