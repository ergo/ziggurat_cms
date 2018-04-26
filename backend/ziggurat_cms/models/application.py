# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from ziggurat_cms.models.resource import Resource


class Application(Resource):
    """
    Resource of application type
    """

    __tablename__ = 'applications'
    __mapper_args__ = {'polymorphic_identity': 'application'}

    __possible_permissions__ = ['view', 'edit']

    resource_id = sa.Column(sa.Integer(),
                            sa.ForeignKey('resources.resource_id',
                                          onupdate='CASCADE',
                                          ondelete='CASCADE', ),
                            primary_key=True)

    description = sa.Column('description', sa.UnicodeText)
    node_info = sa.Column('node_info', postgresql.JSONB, default='{}')
    node_js = sa.Column('node_js', sa.UnicodeText)
    node_css = sa.Column('node_css', sa.UnicodeText)
    node_info_schema_version = sa.Column(
        'node_info_schema_version', sa.Integer, default=1)

    domains = sa.orm.relationship(
        'ApplicationDomain',
        passive_deletes=True,
        passive_updates=True,
        backref='owner',
        lazy='dynamic')
