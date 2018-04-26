# -*- coding: utf-8 -*-

import logging
import os

from pyramid.httpexceptions import HTTPConflict
from pyramid.i18n import TranslationStringFactory
from pyramid.response import FileResponse
from pyramid.view import view_config, view_defaults
from ziggurat_cms.elements.upload_files import ELEMENT_CONFIG
from ziggurat_cms.elements.upload_files.models import ZigguratCMSFileUpload
from ziggurat_cms.elements.upload_files.service import ElementUploadFileService
from ziggurat_cms.models.element_upload import ElementUploadFile
from ziggurat_cms.services.resource import ResourceService
from ziggurat_cms.validation.schemes import UploadSchema, PageElementSchema
from ziggurat_cms.views import BaseView

log = logging.getLogger(__name__)

_ = TranslationStringFactory('ziggurat_cms')


@view_defaults(route_name='api_object', renderer='json',
               permission='view_api',
               match_param=('object=zigguratcms-upload-files-elements',))
class FileUploadElementAPIView(BaseView):
    """
    Views for Gallery typeElement
    """

    def __init__(self, request):
        super(FileUploadElementAPIView, self).__init__(request)

    @view_config(request_method='GET')
    def get(self):
        resource = self.request.context.resource
        schema = PageElementSchema()
        return schema.dump(resource).data

    @view_config(request_method='POST', route_name='api_object_relation',
                 match_param=('relation=zigguratcms-upload-files-elements',
                              'object=resources'))
    def post(self):
        resource = self.request.context.resource
        is_compatible = ResourceService.check_element_classifiers(
            self.request, resource, ELEMENT_CONFIG['element_classifiers'])
        if not is_compatible:
            return HTTPConflict()
        json_body = self.request.json_body
        element_uuid = json_body.get('element_uuid')
        column_uuid = json_body.get('column_uuid')
        row_uuid = json_body.get('row_uuid')
        grid = resource.elements[0]
        found_column = None
        for row in grid.config['rows']:
            if row['uuid'] == row_uuid:
                for column in row['columns']:
                    if column['uuid'] == column_uuid:
                        found_column = column
        if found_column['element_uuids']:
            raise Exception('Disabled')
        node_element = ZigguratCMSFileUpload()
        resource.elements.append(node_element)
        node_element.parent_element_pkey = grid.pkey
        node_element.config = {}
        node_element.persist(flush=True, db_session=self.request.dbsession)
        found_column['element_uuids'].append(node_element.uuid)
        grid.config.changed()
        schema = PageElementSchema()
        return schema.dump(node_element).data

    @view_config(route_name='api_object_relation', renderer='json',
                 permission='view_api', request_method='GET',
                 match_param=(
                         'object=zigguratcms-upload-files-elements',
                         'relation=files'))
    def files_get(self):
        element = self.request.context.element
        schema = UploadSchema()
        return schema.dump(element.files, many=True).data

    @view_config(route_name='api_object_relation', renderer='json',
                 permission='edit_api', request_method='POST',
                 match_param=(
                         'object=zigguratcms-upload-files-elements',
                         'relation=files'))
    def file_post(self):
        uploaded_file = self.request.POST.get('file')
        upload_dir = os.path.join('private', 'zigguratcms-upload-files')
        upload_file = ElementUploadFile(
            name='',
            description='',
            original_filename='',
            slug='',
            upload_path='',
            from_element=ELEMENT_CONFIG['type']
        )
        upload_file.resource_id = self.request.context.resource.resource_id
        self.request.context.element.files.append(upload_file)
        upload_file.filename = 'DUMMY'
        upload_file.persist(flush=True, db_session=self.request.dbsession)
        parsed_name = ElementUploadFileService.gen_filename(
            upload_file.pkey, upload_file.uuid, uploaded_file.filename)
        name = parsed_name.orginal_filename
        if parsed_name.extension:
            name = name[:len(parsed_name.extension) * -1 - 1]

        upload_file.original_filename = parsed_name.orginal_filename
        upload_file.name = name
        upload_file.slug = parsed_name.filename
        upload_file.filename = parsed_name.filename
        upload_file.extension = parsed_name.extension
        absolute_upload_dir = ElementUploadFileService.gen_directory(
            self.request.registry.settings['upload.root_dir'],
            upload_dir, upload_file.pkey)

        root_length = len(self.request.registry.settings['upload.root_dir'])
        upload_file.upload_path = absolute_upload_dir[root_length + 1:]

        ElementUploadFileService.save_file(
            uploaded_file.file, absolute_upload_dir, parsed_name.filename)

        schema = UploadSchema()
        return schema.dump(upload_file).data

    @view_config(route_name='api_object', renderer='json',
                 permission='edit_api', request_method='DELETE',
                 match_param='object=zigguratcms-upload-files-elements-files')
    def file_delete(self):
        file = self.request.context.file
        root_dir = self.request.registry.settings['upload.root_dir']
        ElementUploadFileService.delete_file(root_dir, file.upload_path, file.filename)
        file.delete(db_session=self.request.dbsession)
        return ''

    @view_config(route_name='api_object', renderer='json',
                 permission='edit_api', request_method='PATCH',
                 match_param='object=zigguratcms-upload-files-elements-files')
    def file_patch(self):
        file = self.request.context.file
        json_body = self.request.json_body
        file.populate_obj(json_body, include_keys=['name', 'description'])
        schema = UploadSchema()
        return schema.dump(file).data


@view_defaults(route_name='element', renderer='json',
               permission='view',
               match_param='object=zigguratcms-upload-files-elements-files')
class FileUploadElementView(BaseView):
    def __init__(self, request):
        super(FileUploadElementView, self).__init__(request)

    @view_config(request_method='GET')
    def get(self):
        file = self.request.context.file
        content_type = 'application/octet-stream'
        disposition = 'attachment; filename={}'.format(file.original_filename)
        read_path = os.path.join(
            self.request.registry.settings['upload.root_dir'],
            file.upload_path, file.filename)
        ElementUploadFileService.bump_downloads(file)
        response = FileResponse(read_path,
                                self.request, content_type=content_type)
        response.headers['Content-Disposition'] = disposition
        response.cache_expires(0)
        return response
