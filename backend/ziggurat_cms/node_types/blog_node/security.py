from ziggurat_cms.security import set_base_context_info, set_resource_context


class BlogNodeContext(object):
    pass


def root_factory(request, **kwargs):
    """
    Default security factory for resource nodes
    :param request:
    :return:
    """
    non_id_routes = ['objects', 'api_objects']
    is_base_object_route = request.matched_route and \
                           request.matched_route.name in non_id_routes
    context = BlogNodeContext()
    set_base_context_info(request, context)
    root_resource = context.application if is_base_object_route else None
    set_resource_context(request, context=context, resource=root_resource)
    return context


def slug_factory(request, slug=None, resource=None, **kwargs):
    """
    Default security factory for resource nodes
    :param request:
    :return:
    """
    context = BlogNodeContext()
    set_base_context_info(request, context)
    set_resource_context(request, context=context, resource=resource)
    return context
