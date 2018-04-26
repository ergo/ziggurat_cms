# -*- coding: utf-8 -*-

from __future__ import absolute_import

from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config, view_defaults
from ziggurat_cms.services.resource import ResourceService
from ziggurat_cms.services.resource_tree_service import tree_service
from ziggurat_cms.services.user import UserService
from ziggurat_cms.validation.schemes import (
    ResourceCreateSchema,
    UserResourcePermissionSchema,
    GroupResourcePermissionSchema
)
from ziggurat_cms.views import BaseView
from ziggurat_cms.views.shared.resources import ResourcesShared
from ziggurat_foundations.permissions import ANY_PERMISSION

_ = TranslationStringFactory('ziggurat_cms')


def merge_resource_tree_data(row):
    item = row.Resource.get_dict()
    item['depth'] = row.depth
    return item


@view_defaults(route_name='api_object', renderer='json',
               match_param='object=resources',
               permission='owner_api')
class ResourcesAPI(BaseView):
    def __init__(self, request):
        super().__init__(request)
        self.request = request

    @view_config(route_name='api_object', renderer='json', request_method='GET',
                 match_param='object=resources', permission='view_api')
    def get(self):
        resource = self.request.context.resource
        schema = ResourceCreateSchema()
        return schema.dump(resource).data

    @view_config(route_name='api_objects', request_method='GET',
                 match_param='object=resources', permission='view_api')
    def collection(self):
        resources = tree_service.from_parent_deeper(
            self.request.context.application.resource_id,
            db_session=self.request.dbsession)
        schema = ResourceCreateSchema(context={'request': self.request})
        return schema.dump([merge_resource_tree_data(n) for n in resources], many=True).data

    @view_config(route_name='api_object_relation', renderer='json',
                 match_param=('object=resources', 'relation=children',),
                 permission='view_api')
    def collection_children(self):
        resources = ResourceService.by_parent_id(
            self.request.context.resource.resource_id,
            db_session=self.request.dbsession)
        schema = ResourceCreateSchema(context={'request': self.request})
        return schema.dump(resources, many=True).data


@view_defaults(route_name='api_object_relation', renderer='json',
               match_param=('object=resources', 'relation=permissions',),
               permission='owner_api')
class ResourcesPermissionsAPI(BaseView):
    def __init__(self, request):
        super().__init__(request)
        self.request = request

    @view_config(request_method="GET", permission='authenticated')
    def get(self):
        resource = self.request.context.resource

        is_admin = self.request.has_permission('administrator') or \
                   self.request.has_permission('owner')

        # admin can query everything
        if is_admin and self.request.GET.get('user') != 'self':
            permissions = ResourceService.users_for_perm(
                resource, perm_name=ANY_PERMISSION,
                limit_group_permissions=True, db_session=self.request.dbsession)
        # user can query only own permissions for the resource
        else:
            permissions = ResourceService.perms_for_user(
                resource, self.request.user, db_session=self.request.dbsession)

        permissions_list = []
        for perm in permissions:
            if perm.type == 'user':
                permissions_list.append(
                    {'type': 'user', 'uuid': perm.user.uuid,
                     'perm_name': perm.perm_name})
            elif perm.type == 'group':
                permissions_list.append(
                    {'type': 'group', 'uuid': perm.group.uuid,
                     'perm_name': perm.perm_name})
        return permissions_list


@view_defaults(route_name='api_object_relation', renderer='json',
               match_param=('object=resources', 'relation=user_permissions',),
               permission='owner_api')
class ResourcesUserPermissionsAPI(BaseView):
    def __init__(self, request):
        super().__init__(request)
        self.request = request
        self.shared = ResourcesShared(request)

    @view_config(request_method="GET", permission='__no_permission__')
    def get(self):
        resource = self.request.context.resource

        schema = UserResourcePermissionSchema(
            context={'request': self.request,
                     'resource': resource})
        data = schema.load(self.request.unsafe_json_body).data
        user = UserService.by_prefixed_user_name(
            data['user_name'], db_session=self.request.dbsession)
        perm_inst = self.shared.user_permission_post(
            resource, user.id, data['perm_name'])
        self.request.dbsession.flush()
        return perm_inst.get_dict()

    @view_config(request_method="POST")
    def post(self):
        resource = self.request.context.resource

        schema = UserResourcePermissionSchema(
            context={'request': self.request,
                     'resource': resource})
        data = schema.load(self.request.unsafe_json_body).data
        user = UserService.by_prefixed_user_name(
            data['user_name'], db_session=self.request.dbsession)
        perm_inst = self.shared.user_permission_post(
            resource, user.id, data['perm_name'])
        self.request.dbsession.flush()
        return perm_inst.get_dict()

    @view_config(request_method="DELETE")
    def delete(self):
        resource = self.request.context.resource

        schema = UserResourcePermissionSchema(
            context={'request': self.request,
                     'resource': resource})
        params = {'user_name': self.request.GET.get('user_name'),
                  'perm_name': self.request.GET.get('perm_name')}
        data = schema.load(params).data
        user = UserService.by_prefixed_user_name(
            data['user_name'], db_session=self.request.dbsession)
        self.shared.user_permission_delete(
            resource, user.id, data['perm_name'], )
        return True


@view_defaults(route_name='api_object_relation', renderer='json',
               match_param=('object=resources', 'relation=group_permissions',),
               permission='owner_api')
class ResourcesGroupPermissionsAPI(BaseView):
    def __init__(self, request):
        self.request = request
        self.shared = ResourcesShared(request)

    @view_config(request_method="POST")
    def post(self):
        resource = self.request.context.resource

        schema = GroupResourcePermissionSchema(
            context={'request': self.request,
                     'resource': resource})
        data = schema.load(self.request.unsafe_json_body).data
        perm_inst = self.shared.group_permission_post(
            resource, data['group_id'], data['perm_name'])
        self.request.dbsession.flush()
        return perm_inst.get_dict()

    @view_config(request_method="DELETE")
    def delete(self):
        resource = self.request.context.resource

        schema = GroupResourcePermissionSchema(
            context={'request': self.request,
                     'resource': resource})
        params = {'group_id': self.request.GET.get('group_id'),
                  'perm_name': self.request.GET.get('perm_name')}
        data = schema.load(params).data
        self.shared.group_permission_delete(
            resource, data['group_id'], data['perm_name'])
        return True
