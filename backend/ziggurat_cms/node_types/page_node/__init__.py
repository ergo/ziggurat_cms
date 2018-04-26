# -*- coding: utf-8 -*-
import logging

from ziggurat_cms.constants import ResourceClassifiers
from ziggurat_cms.node_types.page_node.security import (
    root_factory,
    slug_factory
)

log = logging.getLogger(__name__)

NODE_CONFIG = {
    'type': 'zigguratcms-page-node',
    'context_class': None,
    'element_classifiers': [ResourceClassifiers.GRID_SUBELEMENT,
                            ResourceClassifiers.NAVIGABLE],
    'api_base_prefix': 'zigguratcms-page-nodes',
    'api_object_mappings': {
        'zigguratcms-page-node': 'zigguratcms-page-nodes'
    },
    'web_components': [],
    'security_factory': root_factory,
    'node_context_mappings': {
        'zigguratcms-page-node': slug_factory
    }
}


def includeme(config):
    config.cms_register_resource(NODE_CONFIG['type'], NODE_CONFIG)
    config.scan('ziggurat_cms.node_types.page_node')
