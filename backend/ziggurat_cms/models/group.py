# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import uuid
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.hybrid import hybrid_property
from ziggurat_cms.models.meta import Base
from ziggurat_foundations.models.group import GroupMixin


class Group(GroupMixin, Base):
    __possible_permissions__ = (
        'root_administration', 'administration', 'admin_panel', 'admin_users',
        'admin_groups', 'admin_entries')

    uuid = sa.Column('uuid', postgresql.UUID,
                     default=lambda x: str(uuid.uuid4()))
    tenant_pkey = sa.Column('tenant_pkey', sa.Integer,
                                   sa.ForeignKey('resources.resource_id',
                                                 onupdate='CASCADE',
                                                 ondelete='CASCADE'))

    resources = sa.orm.relationship(
        'Resource',
        cascade="all",
        primaryjoin='groups.c.id == resources.c.owner_group_id',
        passive_deletes=True,
        passive_updates=True,
        backref='owner_group')

    resources_dynamic = sa.orm.relationship(
        'Resource',
        cascade="all",
        primaryjoin='groups.c.id == resources.c.owner_group_id',
        passive_deletes=True,
        passive_updates=True,
        lazy='dynamic')

    parent_resource = sa.orm.relationship(
        'Resource',
        passive_deletes=True,
        passive_updates=True,
        primaryjoin='groups.c.tenant_pkey == resources.c.resource_id',
        backref='contains_groups')

    @hybrid_property
    def public_group_name(self):
        return self.group_name[len(str(self.tenant_pkey)) + 1:]

    @public_group_name.setter
    def set_group_name(self, value):
        self.group_name = '{}:{}'.format(self.tenant_pkey, value)

    @sa.orm.validates('group_name')
    def validate_group_name(self, key, value):
        """ validates if group can get assigned with permission"""
        if len(value.split(':')) != 2:
            raise AssertionError('group_name {} is not prefixed'.format(value))
        return value
