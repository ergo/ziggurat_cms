# -*- coding: utf-8 -*-

from pyramid.httpexceptions import HTTPNotFound
from ziggurat_cms.elements.upload_files.service import ElementUploadFileService
from ziggurat_cms.security import set_base_context_info, set_element_context


class UploadFilesContext(object):
    pass


def api_security_factory(request):
    context = UploadFilesContext()
    set_base_context_info(request, context)
    object_type = request.matchdict['object']
    if object_type == 'zigguratcms-upload-files-elements-files':
        file = ElementUploadFileService.by_uuid(
            request.matchdict['uuid'], request.dbsession)
        if file:
            set_element_context(request, context, element=file.element)
            context.file = file
        else:
            return HTTPNotFound()
    else:
        set_element_context(request, context)
    return context
