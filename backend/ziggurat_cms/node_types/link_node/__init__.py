# -*- coding: utf-8 -*-
import logging

from ziggurat_cms.node_types.link_node.security import root_factory, slug_factory

log = logging.getLogger(__name__)

NODE_CONFIG = {
    'type': 'zigguratcms-link-node',
    'context_class': None,
    'element_classifiers': [],
    'api_base_prefix': 'zigguratcms-link-nodes',
    'api_object_mappings': {
        'zigguratcms-link-node': 'zigguratcms-link-nodes'
    },
    'web_components': [],
    'security_factory': root_factory,
    'node_context_mappings': {
        'zigguratcms-link-node': slug_factory
    }
}


def includeme(config):
    config.cms_register_resource(NODE_CONFIG['type'], NODE_CONFIG)
    config.scan('ziggurat_cms.node_types.link_node')
