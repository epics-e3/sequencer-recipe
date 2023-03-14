#!/bin/bash

# LIBVERSION shall only include MAJOR.MINOR.PATCH for require
LIBVERSION=$(echo ${PKG_VERSION}| cut -d'.' -f1-3)

if [[ "$EPICS_TARGET_ARCH" == "linux-ppc64e6500" ]]
then
  # We have to compile for x86 as well (we need to run lemon which is part of seq)
  sed -i "/EXCLUDE_ARCHS=linux-x86_64/d" ${EPICS_BASE}/configure/CONFIG_SITE
fi

# Clean between variants builds
make clean

make MODULE=${PKG_NAME} LIBVERSION=${LIBVERSION}
make MODULE=${PKG_NAME} LIBVERSION=${LIBVERSION} install

