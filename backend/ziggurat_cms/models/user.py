# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import uuid

import sqlalchemy as sa
from pyramid.security import Allow, ALL_PERMISSIONS
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.hybrid import hybrid_property
from ziggurat_cms.models.meta import Base
from ziggurat_foundations.models.user import UserMixin


class User(UserMixin, Base):
    __possible_permissions__ = [
        'root_administration', 'administration', 'admin_panel',
        'admin_users', 'admin_groups', 'admin_entries']

    # registration_ip = sa.Column(sa.Unicode())

    _public_user_name = sa.Column('public_user_name', sa.Unicode(128))
    _public_email = sa.Column('public_email', sa.Unicode(100))

    uuid = sa.Column('uuid', postgresql.UUID,
                     default=lambda x: str(uuid.uuid4()))
    tenant_pkey = sa.Column('tenant_pkey', sa.Integer,
                            sa.ForeignKey('resources.resource_id',
                                          onupdate='CASCADE',
                                          ondelete='CASCADE'))
    auth_tokens = sa.orm.relationship('AuthToken',
                                      cascade="all,delete-orphan",
                                      passive_deletes=True,
                                      passive_updates=True,
                                      backref='owner',
                                      order_by='AuthToken.pkey')

    resources = sa.orm.relationship(
        'Resource',
        cascade="all",
        passive_deletes=True,
        passive_updates=True,
        primaryjoin='users.c.id == resources.c.owner_user_id',
        backref='owner',
        lazy='dynamic')

    parent_resource = sa.orm.relationship(
        'Resource',
        passive_deletes=True,
        passive_updates=True,
        primaryjoin='users.c.tenant_pkey == resources.c.resource_id',
        backref='contains_users')

    def get_dict(self, exclude_keys=None, include_keys=None,
                 permission_info=False):
        if exclude_keys is None:
            exclude_keys = ['user_password', 'security_code',
                            'security_code_date']

        user_dict = super(User, self).get_dict(exclude_keys=exclude_keys,
                                               include_keys=include_keys)
        return user_dict

    @hybrid_property
    def public_user_name(self):
        return self._public_user_name

    @public_user_name.setter
    def public_user_name(self, value):
        if not self.tenant_pkey:
            raise Exception('Tenant primary key is missing')
        self._public_user_name = value
        self.user_name = '{}:{}'.format(self.tenant_pkey, value)

    @hybrid_property
    def public_email(self):
        return self._public_email

    @public_email.setter
    def public_email(self, value):
        if not self.tenant_pkey:
            raise Exception('Tenant primary key is missing')
        self._public_email = value
        self.email = '{}:{}'.format(self.tenant_pkey, value)

    @sa.orm.validates('user_name')
    def validate_user_name(self, key, value):
        """ validates if group can get assigned with permission"""
        if len(value.split(':')) != 2:
            raise AssertionError('user_name {} is not prefixed'.format(value))
        return value

    @sa.orm.validates('email')
    def validate_email(self, key, value):
        """ validates if group can get assigned with permission"""
        if len(value.split(':')) != 2:
            raise AssertionError('email {} is not prefixed'.format(value))
        return value

    @property
    def __acl__(self):
        return [(Allow, self.id, ALL_PERMISSIONS,)]
