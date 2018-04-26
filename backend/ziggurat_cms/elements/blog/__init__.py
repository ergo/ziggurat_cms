# -*- coding: utf-8 -*-
import logging

from ziggurat_cms.constants import ResourceClassifiers
from ziggurat_cms.elements.blog.security import (
    api_security_factory,
    slug_security_factory)

log = logging.getLogger(__name__)

ELEMENT_CONFIG = {
    'type': 'zigguratcms-blog',
    'element_classifiers': [ResourceClassifiers.GRID_SUBELEMENT],
    'context_class': 'zigguratcms.elements.blog.security.BlogContext',
    'api_base_prefix': 'zigguratcms-blog-elements',
    'api_object_mappings': {
        'zigguratcms-blog': 'zigguratcms-blog-elements',
        'zigguratcms-blog-entry': 'zigguratcms-blog-elements-entries',
        'zigguratcms-blog-image': 'zigguratcms-blog-elements-images'
    },
    'web_components': ['zigguratcms-blog'],
    'security_factory': api_security_factory,
    'element_context_mappings': {
        'zigguratcms-blog-entry': slug_security_factory
    }
}


def includeme(config):
    config.cms_register_node_element(
        'ziggurat_cms.elements.blog', element_config=ELEMENT_CONFIG)
    config.scan('ziggurat_cms.elements.blog')
