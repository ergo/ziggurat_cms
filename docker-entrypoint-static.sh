#!/bin/bash
set -e
if [ -n "${USER_UID}" ]; then
  usermod -u $USER_UID application
fi
if [ -n "${USER_GID}" ]; then
  groupmod -g $USER_GID application
fi
cd $STATIC_DIR

gosu application yarn
gosu application yarn bower
gosu application "$@"
