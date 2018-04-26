# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import zope.sqlalchemy
from sqlalchemy import engine_from_config
from sqlalchemy.orm import configure_mappers
from sqlalchemy.orm import sessionmaker
from ziggurat_foundations import ziggurat_model_init

from ziggurat_cms.models.auth_token import AuthToken  # flake8: noqa
from ziggurat_cms.models.application import Application  # flake8: noqa
from ziggurat_cms.models.application_domain import ApplicationDomain  # flake8: noqa
from ziggurat_cms.models.organization import Organization  # flake8: noqa
from ziggurat_cms.models.node_element import NodeElement  # flake8: noqa
from ziggurat_cms.models.element_upload import ElementUpload  # flake8: noqa
from ziggurat_cms.models.element_upload import ElementUploadImage  # flake8: noqa
from ziggurat_cms.models.slug import Slug  # flake8: noqa
from ziggurat_cms.models.external_identity import \
    ExternalIdentity  # flake8: noqa
from ziggurat_cms.models.group import Group  # flake8: noqa
from ziggurat_cms.models.group_permission import \
    GroupPermission  # flake8: noqa
from ziggurat_cms.models.group_resource_permission import \
    GroupResourcePermission  # flake8: noqa
from ziggurat_cms.models.resource import Resource  # flake8: noqa
from ziggurat_cms.models.user import User  # flake8: noqa
from ziggurat_cms.models.user_group import UserGroup  # flake8: noqa
from ziggurat_cms.models.user_permission import UserPermission  # flake8: noqa
from ziggurat_cms.models.user_resource_permission import \
    UserResourcePermission  # flake8: noqa
from ziggurat_foundations import ziggurat_model_init

ziggurat_model_init(User, Group, UserGroup, GroupPermission, UserPermission,
                    UserResourcePermission, GroupResourcePermission, Resource,
                    ExternalIdentity)

# run configure_mappers after defining all of the models to ensure
# all relationships can be setup
configure_mappers()


def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)


def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory


def get_tm_session(session_factory, transaction_manager):
    """
    Get a ``sqlalchemy.orm.Session`` instance backed by a transaction.

    This function will hook the session to the transaction manager which
    will take care of committing any changes.

    - When using pyramid_tm it will automatically be committed or aborted
      depending on whether an exception is raised.

    - When using scripts you should wrap the session in a manager yourself.
      For example::

          import transaction

          engine = get_engine(settings)
          session_factory = get_session_factory(engine)
          with transaction.manager:
              dbsession = get_tm_session(session_factory, transaction.manager)

    """
    dbsession = session_factory()
    zope.sqlalchemy.register(
        dbsession, transaction_manager=transaction_manager)
    return dbsession


def includeme(config):
    """
    Initialize the model for a Pyramid app.

    Activate this setup using ``config.include('ziggurat_cms.models')``.

    """
    settings = config.get_settings()

    # use pyramid_tm to hook the transaction lifecycle to the request
    config.include('pyramid_tm')

    session_factory = get_session_factory(get_engine(settings))
    config.registry['dbsession_factory'] = session_factory

    # make request.dbsession available for use in Pyramid
    config.add_request_method(
        # r.tm is the transaction manager used by pyramid_tm
        lambda r: get_tm_session(session_factory, r.tm),
        'dbsession',
        reify=True
    )
