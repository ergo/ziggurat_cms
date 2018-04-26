from pyramid.security import NO_PERMISSION_REQUIRED


class BaseView(object):
    def __init__(self, request):
        self.request = request
        self.request.handle_cors()
        self.translate = request.localizer.translate


def includeme(config):
    config.add_view(handle_CORS,
                    route_name='CORS_route', renderer='string')
    config.scan('ziggurat_cms.views')
    includes = config.registry.settings.get('pyramid.includes', '')
    if 'pyramid_debugtoolbar' not in includes:
        config.add_view('ziggurat_cms.views.error_handlers.error',
                        context=Exception, permission=NO_PERMISSION_REQUIRED,
                        renderer='json')


def handle_CORS(request):
    request.handle_cors()
    return ''
