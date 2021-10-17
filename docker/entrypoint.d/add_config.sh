#!/bin/bash

#copy fresh config if missing
if [ ! -f /opt/rundir/config.ini ]; then
  set +e
  gosu application ln -s /opt/application/$APP_INI_FILE /opt/rundir/config.ini
  set -e
fi
