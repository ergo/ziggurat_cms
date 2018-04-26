# -*- coding: utf-8 -*-

from ziggurat_cms.security import set_base_context_info, set_element_context


class GridContext(object):
    pass


def api_security_factory(request):
    context = GridContext()
    set_base_context_info(request, context)
    element_uuid = None
    if request.matchdict['object'] in ['zigguratcms-grid-elements-rows',
                                       'zigguratcms-grid-elements-columns']:
        element_uuid = request.GET.get('element')

    set_element_context(request, context, element_uuid=element_uuid)
    return context
