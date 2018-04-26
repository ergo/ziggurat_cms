# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from ziggurat_cms.models.resource import Resource


class PageNode(Resource):
    __tablename__ = 'zigguratcms_page_nodes'
    __mapper_args__ = {'polymorphic_identity': 'zigguratcms-page-node'}

    __possible_permissions__ = ['view', 'edit', 'delete']

    resource_id = sa.Column(sa.Integer(),
                            sa.ForeignKey('resources.resource_id',
                                          onupdate='CASCADE',
                                          ondelete='CASCADE', ),
                            primary_key=True)

    description = sa.Column(sa.UnicodeText, default='')
    node_js = sa.Column(sa.UnicodeText, default='')
    node_css = sa.Column(sa.UnicodeText, default='')
    version = sa.Column('version', sa.Integer, default=1)

    elements = sa.orm.relationship(
        'NodeElement',
        passive_deletes=True,
        passive_updates=True,
        order_by="asc(NodeElement.pkey)",
        lazy='dynamic')

    listed_elements = sa.orm.relationship(
        'NodeElement',
        passive_deletes=True,
        passive_updates=True,
        ## this will filtr out elements like individual blog posts etc.
        primaryjoin="and_(PageNode.resource_id == foreign(NodeElement.resource_id),"
                    "NodeElement.list_for_resource == True)",
        order_by="asc(NodeElement.pkey)",
        lazy='dynamic')
