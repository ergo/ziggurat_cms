# -*- coding: utf-8 -*-
import sqlalchemy as sa

from pyramid.renderers import render
from ziggurat_cms.models.node_element import NodeElement


class ZigguratCMSFileUpload(NodeElement):
    __mapper_args__ = {'polymorphic_identity': 'zigguratcms-upload-files'}

    def render(self, request, resource):
        tmpl_vars = {
            'resource': resource,
            'element': self,
            'element_dict': {e.uuid: e for e in resource.elements}
        }
        rendered = render(
            'ziggurat_cms:elements/upload_files/front_upload_files.jinja2',
            tmpl_vars, request=request)
        return rendered

    files = sa.orm.relationship(
        'ElementUploadFile',
        passive_deletes=True,
        passive_updates=True,
        order_by="asc(ElementUpload.pkey)",
        lazy='dynamic')
