# -*- coding: utf-8 -*-

from __future__ import absolute_import

from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config, view_defaults

from ziggurat_cms.validation.schemes import (
    ApplicationNodeConfigSchema,
    ResourceCreateSchema
)
from ziggurat_cms.views import BaseView

_ = TranslationStringFactory('ziggurat_cms')


@view_defaults(route_name='api_object', renderer='json',
               match_param='object=applications',
               permission='owner_api')
class ApplicationAPI(BaseView):
    def __init__(self, request):
        super().__init__(request)
        self.request = request

    @view_config(route_name='api_object', renderer='json',
                 match_param='object=applications', permission='view_api')
    def patch(self):
        resource = self.request.context.resource
        schema = ApplicationNodeConfigSchema(
            context={'request': self.request, 'modified_obj': resource})
        config_data = self.request.unsafe_json_body.get('config') or {}
        config = schema.load(config_data, partial=True).data
        resource.config = config
        schema = ResourceCreateSchema()
        msg = {'msg': self.translate(_('Application modified')), 'level': 'success'}
        self.request.session.flash(msg)
        return schema.dump(resource).data
