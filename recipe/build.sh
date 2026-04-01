#!/bin/bash

make clean

make MODULE=${PKG_NAME} LIBVERSION=${PKG_VERSION}
make MODULE=${PKG_NAME} LIBVERSION=${PKG_VERSION} install
