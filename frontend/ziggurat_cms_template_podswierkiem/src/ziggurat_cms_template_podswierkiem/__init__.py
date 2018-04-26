import subprocess

import os
import pkg_resources
import shutil


def build_assets(registry, asset_config, *cmd_args, **cmd_kwargs):
    settings = registry.settings
    dest = os.path.join(settings['static.build_dir'], asset_config['type'])
    try:
        shutil.rmtree(dest)
    except FileNotFoundError as exc:
        print(exc)
    shutil.copytree(asset_config['asset_path'], dest,
                    ignore=shutil.ignore_patterns(
                        'node_modules', 'bower_components', '__pycache__'))
    os.environ['ZIGGURAT_CMS_STATIC_DIR'] = settings['static.dir']
    subprocess.check_output(['yarn'], env=os.environ, cwd=dest)
    subprocess.check_output(['node_modules/.bin/gulp'], env=os.environ,
                            cwd=dest)


def includeme(config):
    frontend_config = {
        'type': 'ziggurat_cms_template_podswierkiem',
        'build_script': build_assets, 'web_components': None,
        'asset_path': os.path.abspath(pkg_resources.resource_filename(
            'ziggurat_cms_template_podswierkiem', '../../static_src'))
    }
    config.cms_register_frontend_asset(frontend_config['type'], frontend_config)
