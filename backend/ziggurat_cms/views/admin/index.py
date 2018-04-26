# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from pyramid.i18n import TranslationStringFactory
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from ziggurat_cms.views import BaseView

log = logging.getLogger(__name__)

_ = TranslationStringFactory('ziggurat_cms')


class AdminIndexViews(BaseView):
    @view_config(route_name='admin_index',
                 renderer='ziggurat_cms:templates/admin/index.jinja2',
                 permission=NO_PERMISSION_REQUIRED)
    def index(self):
        element_mappings = {}
        possible_web_components = []
        node_mappings = {}
        for k, element_definition in \
                self.request.registry.cms_element_definitions.items():
            if element_definition['web_components']:
                possible_web_components.extend(element_definition['web_components'])
            if element_definition['api_object_mappings']:
                element_mappings.update(element_definition['api_object_mappings'])
        for k, node_definition in \
                self.request.registry.cms_resource_definitions.items():
            if node_definition['api_object_mappings']:
                node_mappings.update(node_definition['api_object_mappings'])
        return {'possible_web_components': possible_web_components,
                'element_mappings': element_mappings,
                'node_mappings': node_mappings}
