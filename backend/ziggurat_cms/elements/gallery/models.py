# -*- coding: utf-8 -*-
import sqlalchemy as sa

from pyramid.renderers import render
from ziggurat_cms.models.node_element import NodeElement


class ZigguratCMSGallery(NodeElement):
    __mapper_args__ = {'polymorphic_identity': 'zigguratcms-gallery'}

    images = sa.orm.relationship(
        'ElementUploadImage',
        passive_deletes=True,
        passive_updates=True,
        lazy='dynamic')

    def render(self, request, resource):
        tmpl_vars = {
            'resource': resource,
            'element': self,
            'element_dict': {e.uuid: e for e in resource.elements}
        }
        rendered = render(
            'ziggurat_cms:elements/gallery/front_gallery.jinja2',
            tmpl_vars, request=request)
        return rendered
