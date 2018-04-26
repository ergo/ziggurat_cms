# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import uuid

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from ziggurat_cms.constants import StatusEnum
from ziggurat_cms.lib.sqlalchemy import MutableDict
from ziggurat_cms.models.meta import Base
from ziggurat_cms.models.mixins import ModifiedTimesMixin
from ziggurat_foundations.models.base import BaseModel


class NodeElement(Base, ModifiedTimesMixin, BaseModel):
    __tablename__ = 'node_elements'
    __mapper_args__ = {'polymorphic_on': 'type',
                       'with_polymorphic': '*'}

    pkey = sa.Column(sa.Integer(), primary_key=True)

    resource_id = sa.Column(sa.Integer(),
                            sa.ForeignKey('resources.resource_id',
                                          onupdate='CASCADE',
                                          ondelete='CASCADE', ))
    parent_element_pkey = sa.Column(sa.Integer(),
                                    sa.ForeignKey('node_elements.pkey',
                                                  onupdate='CASCADE',
                                                  ondelete='CASCADE', ))
    list_for_resource = sa.Column('list_for_resource', sa.Boolean,
                                  nullable=False, default=True, index=True)
    uuid = sa.Column('uuid', postgresql.UUID,
                     default=lambda x: str(uuid.uuid4()))
    type = sa.Column(sa.Unicode())
    status = sa.Column(sa.SmallInteger(), default=StatusEnum.ACTIVE.value)
    config = sa.Column(MutableDict.as_mutable(postgresql.JSONB), default=dict)
    config_schema_version = sa.Column(
        'config_schema_version', sa.Integer, default=1)
    version = sa.Column('version', sa.Integer, default=1)
    element_js = sa.Column(sa.UnicodeText)
    element_css = sa.Column(sa.UnicodeText)
    current_slug = sa.Column('current_slug', sa.Unicode())

    resource = sa.orm.relationship(
        'Resource',
        passive_deletes=True,
        passive_updates=True,
        uselist=False)

    sub_elements = sa.orm.relationship(
        'NodeElement',
        cascade="all",
        passive_deletes=True,
        passive_updates=True,
        backref=sa.orm.backref('parent_element', remote_side=[pkey]),
        lazy='dynamic')
