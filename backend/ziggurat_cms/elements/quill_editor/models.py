# -*- coding: utf-8 -*-
import sqlalchemy as sa

from pyramid.renderers import render
from ziggurat_cms.models.node_element import NodeElement


class ZigguratCMSQuillEditor(NodeElement):
    __mapper_args__ = {'polymorphic_identity': 'zigguratcms-quill-editor'}

    def render(self, request, resource):
        tmpl_vars = {
            'resource': resource,
            'element': self,
            'element_dict': {e.uuid: e for e in resource.elements}
        }
        rendered = render(
            'ziggurat_cms:elements/quill_editor/front_quill_editor.jinja2',
            tmpl_vars, request=request)
        return rendered

    images = sa.orm.relationship(
        'ElementUploadImage',
        passive_deletes=True,
        passive_updates=True,
        order_by="asc(ElementUploadImage.pkey)",
        lazy='dynamic')
