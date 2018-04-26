# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

import pyramid.httpexceptions
from pyramid.i18n import TranslationStringFactory
from ziggurat_cms.models.group_resource_permission import \
    GroupResourcePermission
from ziggurat_cms.models.user_resource_permission import UserResourcePermission
from ziggurat_cms.services.group_resource_permission import \
    GroupResourcePermissionService
from ziggurat_cms.services.resource import ResourceService
from ziggurat_cms.services.resource_tree_service import tree_service
from ziggurat_cms.services.slug import SlugService
from ziggurat_cms.services.user_resource_permission import \
    UserResourcePermissionService
from ziggurat_foundations import noop

ENTRIES_PER_PAGE = 50

log = logging.getLogger(__name__)

_ = TranslationStringFactory('ziggurat_cms')


class ResourcesShared(object):
    """
    Used by API and admin views
    """

    def __init__(self, request):
        self.request = request
        self.translate = request.localizer.translate
        self.page = 1

    def user_permission_post(self, resource, user_id, perm_name):
        perm_inst = UserResourcePermission(
            user_id=user_id,
            perm_name=perm_name
        )
        resource.user_permissions.append(perm_inst)
        return perm_inst

    def user_permission_get(self, resource_id, user_id, perm_name):
        perm_inst = UserResourcePermissionService.get(
            resource_id=resource_id, user_id=user_id,
            perm_name=perm_name, db_session=self.request.dbsession)
        if not perm_inst:
            raise pyramid.httpexceptions.HTTPNotFound()
        return perm_inst

    def group_permission_get(self, resource_id, group_id, perm_name):
        perm_inst = GroupResourcePermissionService.get(
            resource_id=resource_id, group_id=group_id,
            perm_name=perm_name, db_session=self.request.dbsession)
        if not perm_inst:
            raise pyramid.httpexceptions.HTTPNotFound()
        return perm_inst

    def user_permission_delete(self, resource, user_id, perm_name):
        perm_inst = self.user_permission_get(resource.resource_id, user_id,
                                             perm_name)
        resource.user_permissions.remove(perm_inst)
        return True

    def group_permission_post(self, resource, group_id, permission):
        perm_inst = GroupResourcePermission(
            group_id=group_id,
            perm_name=permission
        )
        resource.group_permissions.append(perm_inst)
        return perm_inst

    def group_permission_delete(self, resource, group_id, perm_name):
        perm_inst = GroupResourcePermissionService.get(
            resource_id=resource.resource_id, group_id=group_id,
            perm_name=perm_name, db_session=self.request.dbsession)
        resource.group_permissions.remove(perm_inst)
        return True

    def shared_post(self, resource, parent_uuid, position):
        parent_resource = ResourceService.by_uuid(
            parent_uuid, db_session=self.request.dbsession)
        resource.parent_id = parent_resource.resource_id
        self.request.user.resources.append(resource)
        resource.persist(flush=True, db_session=self.request.dbsession)
        slug = SlugService.create_slug(
            tenant_pkey=self.request.context.application.resource_id,
            resource_id=resource.resource_id,
            text=resource.resource_name,
            db_session=self.request.dbsession)
        resource.current_slug = slug.prefixed_text

        if position is not None:
            tree_service.set_position(
                resource_id=position.resource_id, to_position=position,
                db_session=self.request.dbsession)
        else:
            # this accounts for the newly inserted row so the total_children
            # will be max+1 position for new row
            total_children = tree_service.count_children(
                resource.parent_id, db_session=self.request.dbsession)
            tree_service.set_position(
                resource_id=resource.resource_id,
                to_position=total_children,
                db_session=self.request.dbsession)

        if hasattr(resource, 'set_defaults'):
            resource.set_defaults(self.request)
        return resource

    def shared_patch(self, resource, parent_uuid, position):
        slug = SlugService.by_text(
            tenant_pkey=self.request.context.application.resource_id,
            text=resource.resource_name, db_session=self.request.dbsession)
        if not slug or slug.prefixed_text != resource.current_slug:
            slug = SlugService.create_slug(
                tenant_pkey=self.request.context.application.resource_id,
                resource_id=resource.resource_id,
                text=resource.resource_name,
                db_session=self.request.dbsession)
            resource.current_slug = slug.prefixed_text

        parent_resource = ResourceService.by_uuid(
            parent_uuid, db_session=self.request.dbsession)
        into_new_parent = parent_uuid != resource.parent_uuid \
                          and parent_uuid is not noop
        if position is not noop or into_new_parent:
            parent_id = parent_resource.resource_id or noop
            if not position and into_new_parent:
                position = tree_service.count_children(
                    parent_id, db_session=self.request.dbsession) + 1
            tree_service.move_to_position(
                resource_id=resource.resource_id, new_parent_id=parent_id,
                to_position=position, db_session=self.request.dbsession)
            # we need to set this manually here because tree_service
            # doesn't do this
            resource.parent_uuid = ResourceService.get(
                parent_id, db_session=self.request.dbsession).uuid
        return resource
