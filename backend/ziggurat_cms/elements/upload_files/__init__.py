# -*- coding: utf-8 -*-
import logging

from ziggurat_cms.constants import ResourceClassifiers
from ziggurat_cms.elements.upload_files.security import api_security_factory

log = logging.getLogger(__name__)


ELEMENT_CONFIG = {
    'type': 'zigguratcms-upload-files',
    'element_classifiers': [ResourceClassifiers.GRID_SUBELEMENT],
    'context_class': 'zigguratcms.elements.upload_files.'
                     'security.UploadFilesContext',
    'web_comonents': ['zigguratcms-upload-files'],
    'api_base_prefix': 'zigguratcms-upload-files-elements',
    'api_object_mappings': {
        'zigguratcms-upload-files': 'zigguratcms-upload-files-elements',
        'zigguratcms-upload-files-file': 'zigguratcms-upload-files-'
                                         'elements-files'
    },
    'security_factory': api_security_factory
}


def includeme(config):
    config.cms_register_node_element(
        'ziggurat_cms.elements.upload_files', element_config=ELEMENT_CONFIG)
    config.scan('ziggurat_cms.elements.upload_files')
