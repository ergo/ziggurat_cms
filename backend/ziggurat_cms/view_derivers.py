def dynamic_template_deriver(view, info):
    """
    puts renderer information onto context object

    :param view:
    :param info:
    :return:
    """
    renderer = info.options.get('renderer')
    renderer_name = renderer.name if renderer else None
    if renderer_name and 'jinja' in renderer_name:
        def wrapper_view(context, request):
            if context:
                context.renderer_name = renderer_name
            response = view(context, request)
            return response
        return wrapper_view
    return view
