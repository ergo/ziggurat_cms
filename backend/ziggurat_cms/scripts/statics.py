from __future__ import print_function
import logging

import os
import shutil
import sys

from pyramid.paster import (
    bootstrap,
    setup_logging,
)
from pyramid.scripts.common import parse_vars


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    env = bootstrap(config_uri)
    registry = env['registry']
    settings = registry.settings
    if not hasattr(registry, 'cms_frontend_assets'):
        print('No static packages registered')
        return
    statics_dict = registry.cms_frontend_assets
    for plugin_name, config in statics_dict.items():
        if config['build_script']:
            print('running build script for {}'.format(plugin_name))
            config['build_script'](registry, config)

    for root, dirs, files in os.walk(settings['static.dir']):
        for item in dirs:
            os.chmod(os.path.join(root, item), 0o775)
        for item in files:
            os.chmod(os.path.join(root, item), 0o664)
    print('DONE BUILDING')
