# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

from pyramid.view import view_config, view_defaults
from pyramid.security import Authenticated

from ziggurat_cms.models.user import User
from ziggurat_cms.lib import safe_integer
from ziggurat_cms.lib.request import gen_pagination_headers
from ziggurat_cms.validation.schemes import (
    UserCreateSchema,
    UserEditSchema,
    UserSearchSchema,
    UserPermissionSchema)

from ziggurat_cms.views import BaseView
from ziggurat_cms.views.shared.users import UsersShared
from ziggurat_cms.lib import safe_uuid

log = logging.getLogger(__name__)


@view_defaults(route_name='api_object', renderer='json',
               permission='admin_users_api',
               match_param='object=users')
class AdminUserAPIView(BaseView):
    def __init__(self, request):
        super().__init__(request)
        self.shared = UsersShared(request)

    @view_config(route_name='api_objects', request_method='GET')
    def collection_list(self):
        schema = UserCreateSchema(context={'request': self.request})
        page = safe_integer(self.request.GET.get('page', 1))
        filter_params = UserSearchSchema().load(self.request.GET.mixed()).data
        user_paginator = self.shared.collection_list(
            tenant_pkey=self.request.context.application.resource_id,
            page=page, filter_params=filter_params
        )
        headers = gen_pagination_headers(request=self.request,
                                         paginator=user_paginator)
        self.request.response.headers.update(headers)
        return schema.dump(user_paginator.items, many=True).data

    @view_config(route_name='api_objects', request_method='POST')
    def post(self):
        schema = UserCreateSchema(context={'request': self.request})
        data = schema.load(self.request.unsafe_json_body).data
        user = User()
        self.shared.populate_instance(user, data)
        user.persist(flush=True, db_session=self.request.dbsession)
        return schema.dump(user).data

    @view_config(permission='view_self_api', request_method='GET',
                 match_param=('object=users', 'uuid=self'))
    def get_self(self):
        user = self.request.user
        schema = UserCreateSchema(context={'request': self.request},
                                  exclude=['id'])
        return schema.dump(user).data

    # we need both views here to have multiple permissions
    @view_config(request_method='GET')
    def get(self):
        user = self.shared.user_get(self.request.matchdict['uuid'])
        schema = UserCreateSchema(context={'request': self.request},
                                  exclude=['id'])
        return schema.dump(user).data

    @view_config(route_name='api_object', request_method="PATCH")
    def patch(self):
        user = self.shared.user_get(safe_uuid(self.request.matchdict['uuid']))
        schema = UserEditSchema(context={'request': self.request,
                                         'modified_obj': user})
        data = schema.load(self.request.unsafe_json_body, partial=True).data
        self.shared.populate_instance(user, data)
        new_email = data.get('public_email')
        if new_email:
            user.public_email = new_email
        return schema.dump(user).data

    @view_config(request_method="DELETE")
    def delete(self):
        user = self.shared.user_get(self.request.matchdict['uuid'])
        self.shared.delete(user)
        return True


@view_defaults(route_name='api_object_relation', renderer='json',
               match_param=('object=users', 'relation=permissions',),
               permission='admin_users_api')
class UsersPermissionsAPI(BaseView):
    def __init__(self, request):
        super().__init__(request)
        self.shared = UsersShared(request)

    @view_config(request_method="GET")
    def get(self):
        user = self.shared.user_get(self.request.matchdict['uuid'])
        schema = UserPermissionSchema()
        return schema.dump(user.permissions, many=True).data

    @view_config(request_method="POST")
    def post(self):
        json_body = self.request.unsafe_json_body
        user = self.shared.user_get(self.request.matchdict['uuid'])
        self.shared.permission_post(user, json_body['perm_name'])
        return True

    @view_config(request_method="DELETE")
    def delete(self):
        user = self.shared.user_get(self.request.matchdict['uuid'])
        permission = self.shared.permission_get(
            user, self.request.GET.get('perm_name'))
        self.shared.permission_delete(user, permission)
        return True
