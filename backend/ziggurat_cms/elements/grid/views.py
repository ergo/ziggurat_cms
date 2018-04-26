# -*- coding: utf-8 -*-

import logging

from pyramid.httpexceptions import HTTPConflict
from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config, view_defaults
from ziggurat_cms.elements.grid import ELEMENT_CONFIG
from ziggurat_cms.elements.grid.service import ZigguratCMSGridService
from ziggurat_cms.services.resource import ResourceService
from ziggurat_cms.validation.schemes import PageElementSchema
from ziggurat_cms.views import BaseView

log = logging.getLogger(__name__)

_ = TranslationStringFactory('ziggurat_cms')


@view_defaults(route_name='api_object', renderer='json',
               permission='view_api',
               match_param=('object=zigguratcms-grid-elements',))
class GridElementAPIView(BaseView):
    """
    Views for GridElement
    """

    def __init__(self, request):
        super(GridElementAPIView, self).__init__(request)

    @view_config(request_method='GET')
    def get(self):
        resource = self.request.context.resource
        schema = PageElementSchema()
        return schema.dump(resource).data

    @view_config(request_method='POST', route_name='api_object_relation',
                 match_param=('relation=zigguratcms-grid-elements',
                              'object=resources'))
    def post(self):
        resource = self.request.context.resource
        is_compatible = ResourceService.check_element_classifiers(
            self.request, resource, ELEMENT_CONFIG['element_classifiers'])
        if not is_compatible:
            return HTTPConflict()
        schema = PageElementSchema()
        return schema.dump(resource).data

    @view_config(request_method='PATCH')
    def patch(self):
        resource = self.request.context.resource
        schema = PageElementSchema()
        return schema.dump(resource).data

    @view_config(route_name='api_object_relation', renderer='json',
                 permission='edit_api', request_method='POST',
                 match_param=(
                         'object=zigguratcms-grid-elements', 'relation=rows'))
    def rows_post(self):
        resource = self.request.context.resource
        element = self.request.context.element
        row = ZigguratCMSGridService.add_row(element)
        return row

    @view_config(route_name='api_object', renderer='json',
                 permission='edit_api', request_method='PATCH',
                 match_param='object=zigguratcms-grid-elements-rows')
    def rows_patch(self):
        resource = self.request.context.resource
        element = self.request.context.element
        row_uuid = self.request.matchdict['uuid']
        data = self.request.json_body
        found_row = ZigguratCMSGridService.patch_row(
            element, row_uuid, data, self.request.dbsession)
        return found_row

    @view_config(route_name='api_object', renderer='json',
                 permission='edit_api', request_method='DELETE',
                 match_param='object=zigguratcms-grid-elements-rows')
    def rows_delete(self):
        resource = self.request.context.resource
        element = self.request.context.element
        row_uuid = self.request.matchdict['uuid']
        ZigguratCMSGridService.delete_row(element, row_uuid,
                                          self.request.dbsession)
        return ''

    @view_config(route_name='api_object_relation', renderer='json',
                 permission='edit_api', request_method='POST',
                 match_param=(
                         'object=zigguratcms-grid-elements-rows',
                         'relation=columns'))
    def columns_post(self):
        resource = self.request.context.resource
        element = self.request.context.element
        column_uuid = self.request.matchdict['uuid']
        column = ZigguratCMSGridService.add_column(column_uuid, element)
        return column

    @view_config(route_name='api_object', renderer='json',
                 permission='edit_api', request_method='DELETE',
                 match_param='object=zigguratcms-grid-elements-columns')
    def columns_delete(self):
        resource = self.request.context.resource
        element = self.request.context.element
        column_uuid = self.request.matchdict['uuid']
        ZigguratCMSGridService.delete_column(element, column_uuid,
                                             self.request.dbsession)
        return ''

    @view_config(route_name='api_object', renderer='json',
                 permission='edit_api', request_method='PATCH',
                 match_param='object=zigguratcms-grid-elements-columns')
    def columns_patch(self):
        resource = self.request.context.resource
        element = self.request.context.element
        column_uuid = self.request.matchdict['uuid']
        data = self.request.json_body
        found_row = ZigguratCMSGridService.patch_column(
            element, column_uuid, data, self.request.dbsession)
        return found_row
