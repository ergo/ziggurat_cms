# -*- coding: utf-8 -*-

from pyramid.httpexceptions import HTTPNotFound
from ziggurat_cms.elements.blog.service import ElementUploadImageService
from ziggurat_cms.security import (set_base_context_info,
                                   set_element_context)


class BlogContext(object):
    pass


class BlogEntryContext(object):
    pass


def api_security_factory(request):
    object_type = request.matchdict['object']
    context = BlogContext()
    set_base_context_info(request, context)
    if object_type == 'zigguratcms-blog-elements-images':
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


def slug_security_factory(request, slug=None, element=None, resource=None):
    context = BlogEntryContext()
    set_base_context_info(request, context)
    context.element = slug.element
    set_element_context(request, context, element=slug.element)
    return context
