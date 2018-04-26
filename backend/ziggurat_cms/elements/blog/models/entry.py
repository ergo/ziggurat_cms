# -*- coding: utf-8 -*-
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as postgresql
from pyramid.renderers import render
from ziggurat_cms.models.node_element import NodeElement


class ZigguratCMSBlogEntry(NodeElement):
    __tablename__ = "zigguratcms_blog_entries"
    __mapper_args__ = {'polymorphic_identity': 'zigguratcms-blog-entry'}

    pkey = sa.Column('pkey', sa.BigInteger(),
                     sa.ForeignKey('node_elements.pkey',
                                   onupdate='CASCADE',
                                   ondelete='CASCADE'), primary_key=True)
    name = sa.Column('name', sa.Unicode(256), default='', nullable=False)
    tags = sa.Column('tags', postgresql.JSONB(), default=list, nullable=False)

    images = sa.orm.relationship(
        'ElementUploadImage',
        passive_deletes=True,
        passive_updates=True,
        lazy='dynamic')

    def render_abstract(self, request, resource):
        tmpl_vars = {
            'resource': resource,
            'element': self,
            'element_dict': {e.uuid: e for e in resource.elements}
        }
        rendered = render(
            'ziggurat_cms:elements/blog/front_blog_entry_abstract.jinja2',
            tmpl_vars, request=request)
        return rendered

    def render(self, request, resource):
        tmpl_vars = {
            'resource': resource,
            'element': self,
            'element_dict': {e.uuid: e for e in resource.elements}
        }
        rendered = render(
            'ziggurat_cms:elements/blog/front_blog_entry.jinja2',
            tmpl_vars, request=request)
        return rendered
