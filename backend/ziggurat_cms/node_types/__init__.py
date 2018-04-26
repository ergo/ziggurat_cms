# -*- coding: utf-8 -*-

import logging

log = logging.getLogger(__name__)


def includeme(config):
    config.include('ziggurat_cms.node_types.page_node')
    config.include('ziggurat_cms.node_types.blog_node')
    config.include('ziggurat_cms.node_types.link_node')
    config.include('ziggurat_cms.node_types.category_node')

