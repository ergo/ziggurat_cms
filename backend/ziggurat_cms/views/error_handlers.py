import logging
from pyramid.renderers import render_to_response
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config

log = logging.getLogger(__name__)


@view_config(context='ziggurat_cms.exceptions.JSONException',
             permission=NO_PERMISSION_REQUIRED, renderer='json')
def invalid_json(context, request):
    request.response.status = 422
    request.handle_cors()
    return 'Incorrect JSON'


@view_config(context='marshmallow.ValidationError',
             permission=NO_PERMISSION_REQUIRED,
             renderer='json')
def marshmallow_invalid_data(context, request):
    request.response.status = 422
    request.handle_cors()
    return context.messages


@view_config(context='passlib.exc.MissingBackendError',
             permission=NO_PERMISSION_REQUIRED,
             renderer='string')
def no_bcrypt_found(context, request):
    request.response.status = 500
    request.handle_cors()
    return str(context)


@view_config(context='pyramid.exceptions.HTTPForbidden',
             permission=NO_PERMISSION_REQUIRED,
             renderer='string')
def forbidden(context, request):
    request.response.status = 403
    request.handle_cors()
    if request.matched_route and request.matched_route.name.startswith('api_'):
        return 'FORBIDDEN'
    return render_to_response(
        'ziggurat_cms:templates/error_handlers/forbidden.jinja2', value={},
        request=request)


def error(context, request):
    request.response.status = 500
    request.handle_cors()
    log.exception(context)
    if request.matched_route and request.matched_route.name.startswith('api_'):
        return 'EXCEPTION'
    return render_to_response(
        'ziggurat_cms:templates/error_handlers/error.jinja2', value={},
        request=request)
