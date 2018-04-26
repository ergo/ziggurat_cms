# -*- coding: utf-8 -*-
import logging

from ziggurat_cms.elements.grid.security import api_security_factory

log = logging.getLogger(__name__)

ELEMENT_CONFIG = {
    'type': 'zigguratcms-grid',
    'element_classifiers': [],
    'context_class': 'zigguratcms.elements.grid.security.GridContext',
    'web_components': ['zigguratcms-grid'],
    'api_base_prefix': 'zigguratcms-grid-elements',
    'api_object_mappings': {
        'zigguratcms-grid': 'zigguratcms-grid-elements'
    },
    'security_factory': api_security_factory
}


def includeme(config):
    config.cms_register_node_element(
        'ziggurat_cms.elements.grid', element_config=ELEMENT_CONFIG)

    config.scan('ziggurat_cms.elements.grid')
