# -*- coding: utf-8 -*-
import logging

from ziggurat_cms.constants import ResourceClassifiers
from ziggurat_cms.elements.quill_editor.security import api_security_factory

log = logging.getLogger(__name__)

ELEMENT_CONFIG = {
    'type': 'zigguratcms-quill-editor',
    'element_classifiers': [ResourceClassifiers.GRID_SUBELEMENT],
    'context_class': 'zigguratcms.elements.quill_editor.security.QillEditorContext',
    'web_components': ['zigguratcms-quill-editor'],
    'api_base_prefix': 'zigguratcms-quill-editor-elements',
    'api_object_mappings': {
        'zigguratcms-quill-editor': 'zigguratcms-quill-editor-elements',
        'zigguratcms-quill-editor-image': 'zigguratcms-quill-editor-elements-images',
    },
    'security_factory': api_security_factory
}


def includeme(config):
    config.cms_register_node_element(
        'ziggurat_cms.elements.quill_editor', element_config=ELEMENT_CONFIG)

    config.scan('ziggurat_cms.elements.quill_editor')
