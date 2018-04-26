# -*- coding: utf-8 -*-
import logging

from ziggurat_cms.node_types.category_node.security import root_factory, slug_factory

log = logging.getLogger(__name__)

NODE_CONFIG = {
    'type': 'zigguratcms-category-node',
    'context_class': None,
    'element_classifiers': [],
    'api_base_prefix': 'zigguratcms-category-nodes',
    'api_object_mappings': {
        'zigguratcms-category-node': 'zigguratcms-category-nodes'
    },
    'web_components': [],
    'security_factory': root_factory,
    'node_context_mappings': {
        'zigguratcms-category-node': slug_factory
    }
}


def includeme(config):
    config.cms_register_resource(NODE_CONFIG['type'], NODE_CONFIG)
    config.scan('ziggurat_cms.node_types.category_node')
