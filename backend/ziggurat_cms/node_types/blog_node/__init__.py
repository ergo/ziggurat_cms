# -*- coding: utf-8 -*-
import logging

from ziggurat_cms.constants import ResourceClassifiers
from ziggurat_cms.node_types.blog_node.security import (
    slug_factory,
    root_factory)

log = logging.getLogger(__name__)

NODE_CONFIG = {
    'type': 'zigguratcms-blog-node',
    'context_class': None,
    'element_classifiers': [ResourceClassifiers.GRID_SUBELEMENT,
                            ResourceClassifiers.NAVIGABLE],
    'api_base_prefix': 'zigguratcms-blog-nodes',
    'api_object_mappings': {
        'zigguratcms-blog-node': 'zigguratcms-blog-nodes'
    },
    'web_components': [],
    'security_factory': root_factory,
    'node_context_mappings': {
        'zigguratcms-blog-node': slug_factory
    }
}


def includeme(config):
    config.cms_register_resource(NODE_CONFIG['type'], NODE_CONFIG)
    config.scan('ziggurat_cms.node_types.blog_node')
