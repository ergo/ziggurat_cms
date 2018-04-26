# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from contextlib import contextmanager
from collections import namedtuple

from ziggurat_cms.models import (
    Group,
    GroupPermission,
    User,
    AuthToken,
    UserPermission)
from ziggurat_cms.models.application import Application
from ziggurat_cms.models.application_domain import ApplicationDomain
from ziggurat_cms.models.organization import Organization
from ziggurat_cms.node_types.page_node.models import PageNode
from ziggurat_cms.services.resource_tree_service import tree_service


def create_default_application(session):
    organization = Organization(resource_name='Root organization')
    organization.persist(flush=True, db_session=session)
    total_children = tree_service.count_children(None, db_session=session)
    tree_service.set_position(
        resource_id=organization.resource_id,
        to_position=total_children, db_session=session)
    application = Application(resource_name='Localhost application')
    application.parent_id = organization.resource_id
    application.persist(flush=True, db_session=session)
    total_children = tree_service.count_children(
        organization.resource_id, db_session=session)
    tree_service.set_position(
        resource_id=application.resource_id, to_position=total_children,
        db_session=session)

    application.domains.append(ApplicationDomain(domain='localhost'))
    application.domains.append(ApplicationDomain(domain='127.0.0.1'))
    application.persist(flush=True, db_session=session)
    return application


def create_admin(tenant_pkey, session):
    admin = create_user(
        tenant_pkey,
        {'public_user_name': 'test', 'public_email': 'test@test.local'},
        permissions=['root_administration'],
        sqla_session=session)
    token = admin.auth_tokens[0].token
    return admin, token


def create_group(tenant_pkey, group_dict, permissions=None, sqla_session=None):
    group = Group()
    group.tenant_pkey = tenant_pkey
    group.populate_obj(group_dict)
    group.public_group_name = group_dict['public_group_name']
    if permissions:
        for perm_name in permissions:
            permission_instance = GroupPermission(perm_name=perm_name)
            group.permissions.append(permission_instance)
    group.persist(flush=True, db_session=sqla_session)
    return group


def create_user(tenant_pkey, user_dict, permissions=None, sqla_session=None):
    user = User()
    user.tenant_pkey = tenant_pkey
    user.populate_obj(user_dict)
    user.public_user_name = user_dict['public_user_name']
    user.public_email = user_dict['public_email']
    user.auth_tokens.append(AuthToken())
    if permissions:
        for perm_name in permissions:
            permission_instance = UserPermission(perm_name=perm_name)
            user.user_permissions.append(permission_instance)
    user.persist(flush=True, db_session=sqla_session)
    return user


def create_page_node(entry_dict, sqla_session=None):
    entry = PageNode(**entry_dict)
    entry.persist(flush=True, db_session=sqla_session)
    return entry


@contextmanager
def session_context(session):
    """Provide a transactional scope around a series of operations."""
    try:
        yield session
        session.commit()
    finally:
        session.rollback()


@contextmanager
def tmp_session_context(session):
    """Provide a transactional scope around a series of operations."""
    try:
        yield session
        session.rollback()
    finally:
        session.rollback()

DefaultAppTuple = namedtuple('DefaultAppTuple',
                           ['application', 'admin', 'token'])

def set_default_app_data(session):
    """
    Provide a default application with localhost domains and admin user
    :param sqla_session:
    :return:
    """
    application = create_default_application(session)
    admin, token = create_admin(application.resource_id, session)
    return DefaultAppTuple(application, admin, token)
