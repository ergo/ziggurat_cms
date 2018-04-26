# -*- coding: utf-8 -*-

from pyramid.httpexceptions import HTTPNotFound
from ziggurat_cms.elements.quill_editor.service import ElementUploadImageService
from ziggurat_cms.security import set_base_context_info, set_element_context


class QillEditorContext(object):
    pass


def api_security_factory(request):
    context = QillEditorContext()
    set_base_context_info(request, context)
    object_type = request.matchdict['object']
    if object_type == 'zigguratcms-quill-editor-elements-images':
        image = ElementUploadImageService.by_uuid(
            request.matchdict['uuid'], request.dbsession)
        if image:
            set_element_context(request, context, element=image.element)
            context.image = image
        else:
            return HTTPNotFound()
    else:
        set_element_context(request, context)
    return context
