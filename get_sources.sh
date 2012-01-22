#!/bin/sh

URL="https://freeorion.svn.sourceforge.net/svnroot/freeorion/trunk/FreeOrion"
NAME=freeorion
SVN_REV=4282
VERSION=0.3.17


svn export -r ${SVN_REV} ${URL} ${NAME}-${VERSION}
tar -czvf ${NAME}-${VERSION}.tar.gz ${NAME}-${VERSION}/
rm -rf ${NAME}-${VERSION}
