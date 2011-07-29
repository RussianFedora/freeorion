#!/bin/sh

NAME=freeorion
SVN_REV=4046

svn co -r ${SVN_REV} https://freeorion.svn.sourceforge.net/svnroot/freeorion/trunk ${NAME} > /dev/null 2>&1
cd ${NAME}

# Get version of gigi
VERSION=`cat FreeOrion/CMakeLists.txt | grep 'set(FREEORION_VERSION' | awk '{print $2}' | sed 's|)||g'`
FULL_NAME=${NAME}-${VERSION}

# Remove .svn
find . -name .svn -exec rm -rf {} \; > /dev/null 2>&1

mv FreeOrion $FULL_NAME
tar cfjv ../${FULL_NAME}.tar.bz2 $FULL_NAME > /dev/null 2>&1
cd ..
rm -rf ${NAME}