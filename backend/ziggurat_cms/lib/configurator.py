import logging

from collections import OrderedDict

log = logging.getLogger(__name__)

# TODO: implement interfaces for that

NODE_CONFIG_KEYS = (
    'type', 'celery_tasks', 'celery_beats', 'fulltext_indexer',
    'web_components', 'sqlalchemy_migrations', 'api_base_prefix',
    'default_values_setter', 'api_object_mappings', 'element_classifiers')

ELEMENT_CONFIG_KEYS = (
    'type', 'celery_tasks', 'celery_beats', 'fulltext_indexer',
    'web_components', 'sqlalchemy_migrations', 'api_base_prefix',
    'default_values_setter', 'api_object_mappings', 'element_classifiers')

FRONTEND_ASSET_CONFIG_KEYS = (
    'type', 'build_script', 'web_components', 'asset_path'
)


def cms_register_node_element(config, plugin_name, element_config):
    registry = config.registry
    if not hasattr('config.registry', 'cms_element_definitions'):
        registry.cms_element_definitions = OrderedDict()

    def register():
        log.info('Registering element: {}'.format(plugin_name))
        if plugin_name not in config.registry.cms_element_definitions:
            to_reg_config = {}

            for key in ELEMENT_CONFIG_KEYS:
                to_reg_config[key] = element_config.get(key, None)

            registry.cms_element_definitions[plugin_name] = to_reg_config
        security_factory = element_config.get('security_factory')
        if security_factory:
            api_prefix = element_config['api_base_prefix']
            registry.zigg_context_factories[api_prefix] = security_factory
        context_mappings = element_config.get('element_context_mappings')
        if context_mappings:
            for elem_type, security_factory in context_mappings.items():
                log.info('mapping element {} to context factory {}'.format(
                    elem_type, security_factory
                ))
                registry.zigg_element_context_mappings[
                    elem_type] = security_factory

    config.action('ziggurat_cms_element={}'.format(plugin_name), register)


def cms_register_resource(config, plugin_name, node_config):
    registry = config.registry
    if not hasattr('config.registry', 'cms_node_definitions'):
        registry.cms_resource_definitions = OrderedDict()

    def register():
        log.info('Registering node: {}'.format(plugin_name))
        if plugin_name not in config.registry.cms_resource_definitions:
            to_reg_config = {}

            for key in NODE_CONFIG_KEYS:
                to_reg_config[key] = node_config.get(key, None)

            registry.cms_resource_definitions[plugin_name] = to_reg_config
        security_factory = node_config.get('security_factory')
        if security_factory:
            api_prefix = node_config['api_base_prefix']
            registry.zigg_context_factories[api_prefix] = security_factory
        context_mappings = node_config.get('node_context_mappings')
        if context_mappings:
            for node_type, security_factory in context_mappings.items():
                log.info('mapping node {} to context factory {}'.format(
                    node_type, security_factory
                ))
                registry.zigg_resource_context_mappings[
                    node_type] = security_factory

    config.action('ziggurat_cms_resource={}'.format(plugin_name), register)


def cms_register_frontend_asset(config, asset_name, asset_config):
    registry = config.registry
    if not hasattr('config.registry', 'cms_frontend_assets'):
        registry.cms_frontend_assets = OrderedDict()

    def register():
        log.info('Registering frontend asset: {}'.format(asset_name))
        if asset_name not in config.registry.cms_element_definitions:
            to_reg_config = {}

            for key in FRONTEND_ASSET_CONFIG_KEYS:
                to_reg_config[key] = asset_config.get(key, None)

            registry.cms_frontend_assets[asset_name] = to_reg_config

    config.action('ziggurat_cms_frontend_asset={}'.format(asset_name), register)
