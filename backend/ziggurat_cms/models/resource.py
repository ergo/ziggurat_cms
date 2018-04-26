# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import uuid

import sqlalchemy as sa
from pyramid.security import Allow, ALL_PERMISSIONS
from sqlalchemy.dialects import postgresql
from ziggurat_cms.constants import StatusEnum
from ziggurat_cms.models.meta import Base
from ziggurat_cms.models.mixins import ModifiedTimesMixin
from ziggurat_foundations.models.resource import ResourceMixin


class Resource(ResourceMixin, ModifiedTimesMixin, Base):
    uuid = sa.Column('uuid', postgresql.UUID,
                     default=lambda x: str(uuid.uuid4()))
    parent_uuid = sa.Column('parent_uuid', postgresql.UUID)
    tenant_pkey = sa.Column('tenant_pkey', sa.Integer)
    status = sa.Column('status', sa.SmallInteger,
                       default=StatusEnum.ACTIVE.value)

    current_slug = sa.Column('current_slug', sa.Unicode())
    config = sa.Column('config', postgresql.JSONB(), default=dict)
    config_schema_version = sa.Column(
        'config_schema_version', sa.Integer, default=1)

    children = sa.orm.relationship(
        'Resource',
        cascade="all",
        passive_deletes=True,
        passive_updates=True,
        order_by='Resource.ordering',
        lazy='dynamic')

    slugs = sa.orm.relationship(
        'Slug',
        cascade="all",
        passive_deletes=True,
        passive_updates=True,
        backref='resource',
        lazy='dynamic')

    @property
    def __acl__(self):
        acls = []

        if self.owner_user_id:
            acls.extend([(Allow, self.owner_user_id, ALL_PERMISSIONS,), ])

        if self.owner_group_id:
            acls.extend([(Allow, "group:%s" % self.owner_group_id,
                          ALL_PERMISSIONS,), ])
        return acls
