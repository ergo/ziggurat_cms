# -*- coding: utf-8 -*-

import logging

log = logging.getLogger(__name__)


def includeme(config):
    config.include('ziggurat_cms.elements.blog')
    config.include('ziggurat_cms.elements.grid')
    config.include('ziggurat_cms.elements.gallery')
    config.include('ziggurat_cms.elements.quill_editor')
    config.include('ziggurat_cms.elements.upload_files')

