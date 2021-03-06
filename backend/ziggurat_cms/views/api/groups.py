# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

from pyramid.view import view_config, view_defaults

from ziggurat_cms.models.group import Group
from ziggurat_cms.validation.schemes import GroupEditSchema
from ziggurat_cms.views import BaseView
from ziggurat_cms.views.shared.groups import GroupsShared

log = logging.getLogger(__name__)

GROUPS_PER_PAGE = 50


@view_defaults(route_name='api_object', renderer='json',
               match_param='object=groups',
               permission='admin_groups_api')
class GroupsAPIView(BaseView):
    def __init__(self, request):
        super().__init__(request)
        self.shared = GroupsShared(request)

    @view_config(route_name='api_objects', request_method='GET')
    def collection_list(self):
        groups = self.shared.collection_list()
        schema = GroupEditSchema(context={'request': self.request})
        return schema.dump([group for group in groups], many=True).data

    @view_config(route_name='api_objects', request_method='POST')
    def post(self):
        schema = GroupEditSchema(context={'request': self.request})
        data = schema.load(self.request.unsafe_json_body).data
        group = Group()
        self.shared.populate_instance(group, data)
        group.persist(flush=True, db_session=self.request.dbsession)
        return schema.dump(group).data

    @view_config(request_method='GET')
    def get(self):
        schema = GroupEditSchema(context={'request': self.request})
        group = self.shared.group_get(self.request.matchdict['uuid'])
        return schema.dump(group).data

    @view_config(request_method="PATCH")
    def patch(self):
        group = self.shared.group_get(self.request.matchdict['uuid'])
        schema = GroupEditSchema(context={'request': self.request,
                                          'modified_obj': group})
        data = schema.load(self.request.unsafe_json_body).data
        self.shared.populate_instance(group, data)
        return schema.dump(group).data

    @view_config(request_method="DELETE")
    def delete(self):
        group = self.shared.group_get(self.request.matchdict['uuid'])
        self.shared.delete(group)
        return True


@view_defaults(route_name='api_object_relation', renderer='json',
               match_param=('object=groups', 'relation=permissions',),
               permission='admin_groups_api')
class GroupsPermissionsAPI(object):
    def __init__(self, request):
        self.request = request
        self.shared = GroupsShared(request)

    @view_config(request_method="POST")
    def post(self):
        json_body = self.request.unsafe_json_body
        group = self.shared.group_get(self.request.matchdict['uuid'])
        self.shared.permission_post(group, json_body['perm_name'])
        return True

    @view_config(request_method="DELETE")
    def delete(self):
        group = self.shared.group_get(self.request.matchdict['uuid'])
        permission = self.shared.permission_get(
            group, self.request.GET.get('perm_name'))
        self.shared.permission_delete(group, permission)
        return True


@view_defaults(route_name='api_object_relation', renderer='json',
               match_param=('object=groups', 'relation=users',),
               permission='admin_groups_api')
class GroupsUserRelationAPI(object):
    def __init__(self, request):
        self.request = request
        self.shared = GroupsShared(request)

    @view_config(request_method="POST")
    def post(self):
        json_body = self.request.unsafe_json_body
        group = self.shared.group_get(self.request.matchdict['uuid'])
        user = self.shared.user_get_by_username(json_body.get('user_name'))
        self.shared.user_post(group, user)
        return True

    @view_config(request_method="DELETE")
    def delete(self):
        group = self.shared.group_get(self.request.matchdict['uuid'])
        user = self.shared.user_get_by_username(
            self.request.GET.get('user_name'))
        self.shared.user_delete(group, user)
        return True
