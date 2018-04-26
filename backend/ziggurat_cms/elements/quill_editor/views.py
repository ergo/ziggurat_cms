# -*- coding: utf-8 -*-


import logging
import os

from pyramid.httpexceptions import HTTPConflict
from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config, view_defaults
from ziggurat_cms.elements.quill_editor import ELEMENT_CONFIG
from ziggurat_cms.elements.quill_editor.models import ZigguratCMSQuillEditor
from ziggurat_cms.elements.quill_editor.service import (
    ZigguratCMSQuillEditorService,
    ElementUploadImageService)
from ziggurat_cms.models.element_upload import ElementUploadImage
from ziggurat_cms.services.resource import ResourceService
from ziggurat_cms.validation.schemes import UploadImageSchema, PageElementSchema
from ziggurat_cms.views import BaseView

log = logging.getLogger(__name__)

_ = TranslationStringFactory('ziggurat_cms')


@view_defaults(route_name='api_object', renderer='json',
               permission='view_api',
               match_param=('object=zigguratcms-quill-editor-elements',))
class QuillElementAPIView(BaseView):
    """
    Views for QuillElement
    """

    def __init__(self, request):
        super(QuillElementAPIView, self).__init__(request)

    @view_config(request_method='GET')
    def get(self):
        resource = self.request.context.resource
        schema = PageElementSchema()
        return schema.dump(resource).data

    @view_config(request_method='POST', route_name='api_object_relation',
                 match_param=('relation=zigguratcms-quill-editor-elements',
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
        node_element = ZigguratCMSQuillEditor()
        ZigguratCMSQuillEditorService.set_defaults(node_element)
        resource.elements.append(node_element)
        node_element.parent_element_pkey = grid.pkey
        node_element.persist(flush=True, db_session=self.request.dbsession)
        found_column['element_uuids'].append(node_element.uuid)
        grid.config.changed()
        schema = PageElementSchema()
        return schema.dump(node_element).data

    @view_config(request_method='PATCH', permission='edit_api')
    def patch(self):
        resource = self.request.context.resource
        element = self.request.context.element
        json_body = self.request.json_body
        element.config['compiled_html'] = json_body['config']['compiledHtml']
        element.config['delta'] = json_body['config']['delta']
        schema = PageElementSchema()
        return schema.dump(resource).data

    @view_config(route_name='api_object_relation', renderer='json',
                 permission='view_api', request_method='GET',
                 match_param=(
                         'object=zigguratcms-quill-editor-elements',
                         'relation=images'))
    def images_get(self):
        element = self.request.context.element
        schema = UploadImageSchema()
        return schema.dump(element.images, many=True).data

    @view_config(route_name='api_object_relation', renderer='json',
                 permission='edit_api', request_method='POST',
                 match_param=(
                         'object=zigguratcms-quill-editor-elements',
                         'relation=images'))
    def image_post(self):
        uploaded_file = self.request.POST.get('file')
        upload_dir = os.path.join('public', 'zigguratcms-quill-editor')
        upload_image = ElementUploadImage(
            name='',
            description='',
            original_filename='',
            slug='',
            upload_path='',
            from_element=ELEMENT_CONFIG['type']
        )
        upload_image.resource_id = self.request.context.resource.resource_id
        self.request.context.element.images.append(upload_image)
        upload_image.filename = 'DUMMY'
        upload_image.persist(flush=True, db_session=self.request.dbsession)

        parsed_name = ElementUploadImageService.gen_filename(
            upload_image.pkey, upload_image.uuid, uploaded_file.filename)
        name = parsed_name.orginal_filename
        if parsed_name.extension:
            name = name[:len(parsed_name.extension) * -1 - 1]

        upload_image.original_filename = parsed_name.orginal_filename
        upload_image.name = name
        upload_image.slug = parsed_name.filename
        upload_image.filename = parsed_name.filename
        upload_image.extension = parsed_name.extension
        absolute_upload_dir = ElementUploadImageService.gen_directory(
            self.request.registry.settings['upload.root_dir'],
            upload_dir, upload_image.pkey)

        root_length = len(self.request.registry.settings['upload.root_dir'])
        upload_image.upload_path = absolute_upload_dir[root_length + 1:]

        img = ElementUploadImageService.get_image_obj(uploaded_file.file)

        # handle image
        max_size = (1600, 1600)
        ElementUploadImageService.save_resized_image(
            img, parsed_name.filename, absolute_upload_dir, max_size=max_size)

        # handle miniature
        max_size = (128, 128)
        miniature_parsed_name = ElementUploadImageService.gen_filename(
            upload_image.pkey, upload_image.uuid, 'miniature.jpg')
        upload_image.miniature_filename = miniature_parsed_name.filename
        ElementUploadImageService.save_resized_image(
            img, miniature_parsed_name.filename,
            absolute_upload_dir, max_size=max_size)
        base64_encoded = ElementUploadImageService.base64_thumbnail(
            img, (16, 16))
        upload_image.base64_miniature = base64_encoded
        schema = UploadImageSchema()
        return schema.dump(upload_image).data

    @view_config(route_name='api_object', renderer='json',
                 permission='edit_api', request_method='DELETE',
                 match_param='object=zigguratcms-quill-editor-elements-images')
    def image_delete(self):
        image = self.request.context.image
        root_dir = self.request.registry.settings['upload.root_dir']
        ElementUploadImageService.delete_file(
            root_dir, image.upload_path, image.filename)
        ElementUploadImageService.delete_file(
            root_dir, image.upload_path, image.miniature_filename)
        image.delete(db_session=self.request.dbsession)
        return ''
