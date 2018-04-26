# -*- coding: utf-8 -*-

from pyramid.renderers import render
from ziggurat_cms.models.node_element import NodeElement


class ZigguratCMSGrid(NodeElement):
    __mapper_args__ = {'polymorphic_identity': 'zigguratcms-grid'}

    def render(self, request, resource):
        tmpl_vars = {
            'resource': resource,
            'element': self,
            'element_dict': {e.uuid: e for e in resource.elements}
        }
        rendered = render(
            'ziggurat_cms:elements/grid/front_grid.jinja2',
            tmpl_vars, request=request)
        return rendered
