# -*- coding: utf-8 -*-
import logging

from ziggurat_cms.constants import ResourceClassifiers
from ziggurat_cms.elements.gallery.security import api_security_factory

log = logging.getLogger(__name__)

ELEMENT_CONFIG = {
    'type': 'zigguratcms-gallery',
    'element_classifiers': [ResourceClassifiers.GRID_SUBELEMENT],
    'context_class': 'zigguratcms.elements.gallery.security.GalleryContext',
    'api_base_prefix': 'zigguratcms-gallery-elements',
    'api_object_mappings': {
        'zigguratcms-gallery': 'zigguratcms-gallery-elements',
        'zigguratcms-gallery-image': 'zigguratcms-gallery-elements-images'
    },
    'web_components': ['zigguratcms-gallery'],
    'security_factory': api_security_factory
}


def includeme(config):
    config.cms_register_node_element(
        'ziggurat_cms.elements.gallery', element_config=ELEMENT_CONFIG)
    config.scan('ziggurat_cms.elements.gallery')
