import pkg_resources
import os
from ziggurat_cms.lib.cli import build_assets


def includeme(config):
    frontend_config = {
        'type': 'ziggurat_cms_front_admin',
        'build_script': build_assets, 'web_components': None,
        'asset_path': os.path.abspath(pkg_resources.resource_filename(
            'ziggurat_cms_front_admin', '../../static_src'))
    }
    config.cms_register_frontend_asset(frontend_config['type'], frontend_config)
