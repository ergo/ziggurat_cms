# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config, view_defaults
from ziggurat_foundations import noop

from ziggurat_cms.elements.grid.models import ZigguratCMSGrid
from ziggurat_cms.elements.grid.service import ZigguratCMSGridService
from ziggurat_cms.node_types.page_node.models import PageNode
from ziggurat_cms.node_types.page_node.schemes import PageNodeCreateSchema
from ziggurat_cms.node_types.page_node.schemes import PageNodeGETSchema
from ziggurat_cms.services.application import ApplicationService
from ziggurat_cms.services.resource_tree_service import tree_service
from ziggurat_cms.views import BaseView
from ziggurat_cms.views.shared.resources import ResourcesShared

log = logging.getLogger(__name__)

_ = TranslationStringFactory('ziggurat_cms')

CONTEXT_TYPE = 'ziggurat_cms.node_types.page_node.security.PageNodeContext'


def find_elem_data(elem_list, elem_uuids):
    data = []
    for elem_uuid in elem_uuids:
        for item in elem_list:
            if item['uuid'] in elem_uuid:
                data.append(item)
    return data


@view_defaults(route_name='api_object', renderer='json',
               permission='view_api',
               match_param='object=zigguratcms-page-nodes')
class PageNodesAPIView(BaseView):
    """
    Views for nageNode type resources
    """

    def __init__(self, request):
        super(PageNodesAPIView, self).__init__(request)
        # self.shared = PageNodesShared(request)
        self.resources_shared = ResourcesShared(request)

    @view_config(context=CONTEXT_TYPE, permission='view_api')
    def get(self):
        resource = self.request.context.resource
        schema = PageNodeGETSchema()
        data = schema.dump(resource).data
        return data

    @view_config(route_name='api_objects', request_method='POST',
                 match_param='object=zigguratcms-page-nodes',
                 permission='edit_api')
    def post(self):
        resource = self.request.context.resource

        schema = PageNodeCreateSchema(
            context={'request': self.request,
                     'resource': resource})
        json_body = self.request.unsafe_json_body
        data = schema.load(json_body).data
        new_node = PageNode()
        new_node.populate_obj(data)
        new_node.tenant_pkey = self.request.context.application.resource_id
        parent_uuid = data['parent_uuid']
        position = data.get('ordering')
        self.resources_shared.shared_post(new_node, parent_uuid, position)

        node_element = ZigguratCMSGrid()
        ZigguratCMSGridService.set_defaults(node_element)
        new_node.elements.append(node_element)

        msg = {'msg': self.translate(_('Node created')),
               'level': 'success'}
        self.request.session.flash(msg)
        return schema.dump(new_node).data

    @view_config(request_method='PATCH', permission='edit_api',
                 context=CONTEXT_TYPE)
    def patch(self):
        resource = self.request.context.resource
        schema = PageNodeCreateSchema(
            context={'request': self.request, 'modified_obj': resource})
        data = schema.load(self.request.unsafe_json_body, partial=True).data
        # we need to ensure we are not overwriting the values
        # before move_to_position is invoked
        position = data.pop('ordering', None) or noop
        parent_uuid = data.pop('parent_uuid', None) or noop
        resource.populate_obj(data, exclude_keys=['ordering', 'parent_id'])
        self.resources_shared.shared_patch(resource, parent_uuid, position)
        return schema.dump(resource).data

    @view_config(request_method="DELETE", permission='delete_api',
                 context=CONTEXT_TYPE)
    def delete(self):
        resource = self.request.context.resource

        log.info('resource_delete',
                 extra={'resource_id': resource.resource_id,
                        'resource_name': resource.resource_name})
        self.request.session.flash(
            {'msg': self.translate(_('Resource removed.')),
             'level': 'success'})

        tree_service.delete_branch(
            resource.resource_id, db_session=self.request.dbsession)
        return True


class PageNodeViews(BaseView):
    @view_config(route_name='object_slug', context=CONTEXT_TYPE,
                 permission='view',
                 renderer='ziggurat_cms:templates/templated_node.jinja2')
    @view_config(context=CONTEXT_TYPE, permission='view',
                 renderer='ziggurat_cms:templates/templated_node.jinja2')
    def get(self):
        request = self.request
        resource = self.request.context.resource
        result = tree_service.from_parent_deeper(
            resource.resource_id,
            limit_depth=2, db_session=request.dbsession)
        tree = tree_service.build_subtree_strut(result)

        breadcrumbs = tree_service.path_upper(
            resource.resource_id, db_session=request.dbsession).all()[:-2]

        elements = resource.elements.all()
        view_title = ApplicationService.get_title(
            self.request.context.application)
        title = '{}: {}'.format(view_title, resource.resource_name)
        return {
            'zigguratcms_view_title': title,
            'resource': resource,
            'breadcrumbs': breadcrumbs,
            'menu_entries': tree['children'],
            'elements': elements}
