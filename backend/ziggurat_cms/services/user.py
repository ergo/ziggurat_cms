# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from uuid import UUID

import sqlalchemy as sa
from paginate_sqlalchemy import SqlalchemyOrmPage
from ziggurat_foundations.models.services.user import UserService as UService

from ziggurat_cms.models.user import User

log = logging.getLogger(__name__)


class UserService(UService):
    @classmethod
    def by_prefixed_user_name(cls, user_name, tenant_pkey, db_session=None):
        """
        fetch user by user name

        :param user_name:
        :param db_session:
        :return:
        """
        query = db_session.query(cls.model)
        prefixed_user_name = '{}:{}'.format(
            tenant_pkey, user_name or '').lower()
        query = query.filter(
            sa.func.lower(cls.model.user_name) == prefixed_user_name)
        query = query.options(sa.orm.eagerload('groups'))
        return query.first()

    @classmethod
    def by_prefixed_email(cls, email, tenant_pkey, db_session=None):
        """
        fetch user object by email

        :param email:
        :param db_session:
        :return:
        """
        prefixed_email = '{}:{}'.format(
            tenant_pkey, email or '').lower()
        query = db_session.query(cls.model).filter(
            sa.func.lower(cls.model.email) == prefixed_email)
        query = query.options(sa.orm.eagerload('groups'))
        return query.first()

    @classmethod
    def get(cls, user_id, db_session=None):
        """ get user by primary key from session """
        if not user_id:
            return None
        query = db_session.query(cls.model)
        query = query.options(sa.orm.eagerload('groups'))
        return query.get(user_id)

    @classmethod
    def latest_registered_user(cls, db_session=None):
        return db_session.query(User).order_by(sa.desc(User.id)).first()

    @classmethod
    def latest_logged_user(cls, db_session=None):
        return db_session.query(User).order_by(
            sa.desc(User.last_login_date)).first()

    @classmethod
    def total_count(cls, db_session=None):
        return db_session.query(User).count()

    @classmethod
    def get_paginator(cls, tenant_pkey, page=1, item_count=None, items_per_page=50,
                      db_session=None,
                      filter_params=None, **kwargs):
        """ returns paginator over users belonging to the group"""
        if filter_params is None:
            filter_params = {}
        query = db_session.query(User)
        query = query.filter(User.tenant_pkey == tenant_pkey)
        user_name_like = filter_params.get('user_name_like')
        if user_name_like:
            query = query.filter(User.public_user_name.like(user_name_like + '%'))
        query = query.order_by(User.id)

        return SqlalchemyOrmPage(query, page=page, item_count=item_count,
                                 items_per_page=items_per_page,
                                 **kwargs)

    @classmethod
    def permission_info(cls, user):
        return {
            'system_permissions': [p.perm_name for p in user.permissions],
            'resource_permissions': user.resources_with_perms(['owner'])
        }

    @classmethod
    def by_uuid(cls, uuid, db_session=None):
        return db_session.query(cls.model).filter(
            cls.model.uuid == str(uuid)).first()
