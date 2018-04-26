import os
import sys

import transaction
from pyramid.paster import (
    get_appsettings,
    setup_logging,
)
from pyramid.scripts.common import parse_vars
from ziggurat_cms.models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)
from ziggurat_cms.models.application import Application
from ziggurat_cms.models.application_domain import ApplicationDomain
from ziggurat_cms.models.group import Group
from ziggurat_cms.models.group_permission import GroupPermission
from ziggurat_cms.models.group_resource_permission import \
    GroupResourcePermission
from ziggurat_cms.models.organization import Organization
from ziggurat_cms.models.auth_token import AuthToken
from ziggurat_cms.models.user import User
from ziggurat_cms.models.user_permission import UserPermission
from ziggurat_cms.services.resource_tree_service import tree_service
from ziggurat_cms.services.application import ApplicationService

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, name='ziggurat_cms',
                               options=options)

    engine = get_engine(settings)

    session_factory = get_session_factory(engine)
    dbsession = get_tm_session(session_factory, transaction.manager)

    with transaction.manager:

        # GLOBAL ORGANIZATION PERMISSIONS

        organization = Organization(resource_name='Root organization')
        organization.persist(flush=True, db_session=dbsession)
        total_children = tree_service.count_children(None, db_session=dbsession)
        tree_service.set_position(
            resource_id=organization.resource_id,
            to_position=total_children, db_session=dbsession)


        global_admin = User()
        global_admin.tenant_pkey = organization.resource_id
        global_admin.public_user_name = 'admin'
        global_admin.public_email = 'foo@localhost'
        global_admin.set_password('admin')
        global_admin.persist(flush=True, db_session=dbsession)
        global_admin.auth_tokens.append(AuthToken())
        user_permission = UserPermission(perm_name='root_administration')
        global_admin.user_permissions.append(user_permission)
        organization.owner_user_id = global_admin.id

        admin_object = Group()
        admin_object.tenant_pkey = organization.resource_id
        admin_object.public_group_name = 'Global Administrators'
        admin_object.persist(flush=True, db_session=dbsession)
        group_permission = GroupPermission(perm_name='root_administration')
        admin_object.permissions.append(group_permission)
        admin_object.users.append(global_admin)

        # DEFAULT ORGANIZATION LEVEL PERMISSIONS

        organization = Organization(resource_name='Default organization')
        organization.persist(flush=True, db_session=dbsession)
        total_children = tree_service.count_children(None, db_session=dbsession)
        tree_service.set_position(
            resource_id=organization.resource_id,
            to_position=total_children, db_session=dbsession)

        admin = User()
        admin.tenant_pkey = organization.resource_id
        admin.public_user_name = 'admin'
        admin.public_email = 'foo@localhost'
        admin.set_password('admin')
        admin.persist(flush=True, db_session=dbsession)
        user_permission = UserPermission(perm_name='root_administration')
        admin.user_permissions.append(user_permission)
        organization.owner_user_id = admin.id
        admin.auth_tokens.append(AuthToken())

        admin_object = Group()
        admin_object.tenant_pkey = organization.resource_id
        admin_object.public_group_name = 'Administrators'
        admin_object.persist(flush=True, db_session=dbsession)
        group_permission = GroupPermission(perm_name='root_administration')
        admin_object.permissions.append(group_permission)
        admin_object.users.append(global_admin)

        # DEFAULT APPLICATION LEVEL PERMISSIONS

        application = Application(resource_name='Default application')
        application.parent_id = organization.resource_id
        ApplicationService.set_defaults(application)
        application.persist(flush=True, db_session=dbsession)
        total_children = tree_service.count_children(
            organization.resource_id, db_session=dbsession)
        tree_service.set_position(
            resource_id=application.resource_id, to_position=total_children,
            db_session=dbsession)

        application.domains.append(ApplicationDomain(domain='localhost'))
        application.domains.append(ApplicationDomain(domain='127.0.0.1'))

        app_user = User()
        app_user.tenant_pkey = application.resource_id
        app_user.public_user_name = 'admin'
        app_user.public_email = 'foo@localhost'
        app_user.set_password('admin')
        app_user.auth_tokens.append(AuthToken())

        admin_object = Group()
        admin_object.tenant_pkey = application.resource_id
        admin_object.public_group_name = 'Administrators'
        admin_object.persist(flush=True, db_session=dbsession)
        group_resource_permission = GroupResourcePermission(
            resource_id=application.resource_id,
            perm_name='administration')
        admin_object.resource_permissions.append(group_resource_permission)
        group_permission = GroupPermission(perm_name='administration')
        admin_object.permissions.append(group_permission)
        admin_object.users.append(app_user)


        group_object = Group()
        group_object.tenant_pkey = application.resource_id
        group_object.public_group_name = '__UNAUTHORIZED__'
        group_object.persist(flush=True, db_session=dbsession)
        group_object = Group()
        group_object.tenant_pkey = application.resource_id
        group_object.public_group_name = '__AUTHORIZED__'
        group_object.persist(flush=True, db_session=dbsession)
