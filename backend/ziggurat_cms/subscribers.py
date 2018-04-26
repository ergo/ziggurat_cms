# -*- coding: utf-8 -*-

import json

import pkg_resources
from pyramid.events import subscriber, BeforeRender, NewRequest, NewResponse
from pyramid.i18n import TranslationStringFactory
from pyramid.renderers import render
from pyramid.threadlocal import get_current_request
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

from ziggurat_cms.constants import ResourceClassifiers
from ziggurat_cms.events import EmailEvent, SocialAuthEvent
from ziggurat_cms.models.external_identity import ExternalIdentity
from ziggurat_cms.services.external_identity import \
    ExternalIdentityService
from ziggurat_cms.services.resource_tree_service import tree_service
from ziggurat_cms.validation.forms import UserLoginForm

_ = TranslationStringFactory('ziggurat_cms')


@subscriber(EmailEvent)
def email_handler(event):
    mailer = get_mailer(event.request)
    settings = event.request.registry.settings
    rendered = render(event.tmpl_loc, event.tmpl_vars,
                      request=event.request)
    message = Message(subject=event.tmpl_vars['email_title'],
                      sender=settings['mailing.from_email'],
                      recipients=event.recipients,
                      html=rendered)
    if not event.send_immediately:
        mailer.send(message)
    else:
        mailer.send_immediately(message, fail_silently=event.fail_silently)


@subscriber(SocialAuthEvent)
def handle_social_data(event):
    social_data = event.social_data
    request = event.request

    if not social_data['user']['id']:
        request.session.flash(
            _('No external user id found? Perhaps permissions for '
              'authentication are set incorrectly'), 'error')
        return False

    extng_id = ExternalIdentityService.by_external_id_and_provider(
        social_data['user']['id'],
        social_data['credentials'].provider_name,
        db_session=request.dbsession
    )
    update_identity = False
    # if current token doesn't match what we have in db - remove old one
    if extng_id and extng_id.access_token != social_data['credentials'].token:
        extng_id.delete()
        update_identity = True

    if not extng_id or update_identity:
        if not update_identity:
            request.session.flash({'msg': _('Your external identity is now '
                                            'connected with your account'),
                                   'level': 'warning'})
        ex_identity = ExternalIdentity()
        ex_identity.external_id = social_data['user']['id']
        ex_identity.external_user_name = social_data['user']['user_name']
        ex_identity.provider_name = social_data['credentials'].provider_name
        ex_identity.access_token = social_data['credentials'].token
        ex_identity.token_secret = social_data['credentials'].token_secret
        ex_identity.alt_token = social_data['credentials'].refresh_token
        event.user.external_identities.append(ex_identity)
        request.session.pop('zigg.social_auth', None)


def menu_parent_link(request, breadcrumbs):
    breadcrumbs = breadcrumbs[1:] if breadcrumbs else []
    found = None
    definitions = request.registry.cms_resource_definitions
    for node in reversed(breadcrumbs):
        node_definition = definitions[node.resource_type]
        if ResourceClassifiers.NAVIGABLE in node_definition[
            'element_classifiers']:
            found = node
            break

    if found:
        return request.route_path('object_slug', slug=node.current_slug)
    return request.route_path('/')


def pick_template_package(request, template_package, template_name):
    alt_package = None
    if ':' in template_name and template_package:
        package = template_name.split(':', 1)[0]
        test_resource = template_name.replace(package, template_package, 1)
        resource = test_resource[len(template_package)+1:]
        try:
            if pkg_resources.resource_exists(template_package, resource):
                alt_package = test_resource
        except ImportError as exc:
            pass
    return alt_package or template_name


def pick_view_title(request, title):
    if title:
        return title
    if request.context.application:
        return request.context.application.resource_name
    return ''


@subscriber(BeforeRender)
def add_globals(event):
    request = event.get('request') or get_current_request()
    flash_messages = request.session.peek_flash()
    event['pick_template_package'] = pick_template_package
    event['pick_view_title'] = pick_view_title
    if 'zigguratcms_view_title' not in event:
        event['zigguratcms_view_title'] = ''

    event['layout_login_form'] = None
    event['flash_messages'] = flash_messages
    event['base_url'] = request.registry.settings['base_url']
    event['top_node_tree'] = []
    event['top_nodes'] = []
    event['is_index'] = request.matched_route and \
                        request.matched_route.name == '/'
    event['menu_parent_link'] = menu_parent_link

    if request.context.application:
        result = tree_service.from_parent_deeper(
            request.context.application.resource_id,
            limit_depth=2, db_session=request.dbsession)
        tree = tree_service.build_subtree_strut(result)
        event['top_nodes'] = tree['children']

    # we only need to instantiate the form if user is unlogged
    if hasattr(request, 'user') and not request.user:
        event['layout_login_form'] = UserLoginForm(
            request.POST, context={'request': request})


@subscriber(NewRequest)
def new_request(event):
    environ = event.request.environ
    event.request.response.headers[str('X-Frame-Options')] = str('SAMEORIGIN')
    event.request.response.headers[str('X-XSS-Protection')] = str(
        '1; mode=block')
    if environ['wsgi.url_scheme'] == 'https':
        event.request.response.set_cookie(
            'XSRF-TOKEN', event.request.session.get_csrf_token(), secure=True)
    else:
        event.request.response.set_cookie(
            'XSRF-TOKEN', event.request.session.get_csrf_token())
    if event.request.user:
        event.request.response.headers[str('x-user-uuid')] = str(
            event.request.user.uuid)


@subscriber(NewResponse)
def new_response(event):
    request = event.request
    response = event.response
    if request.keep_flash:
        flash_messages = request.session.peek_flash()
    else:
        flash_messages = request.session.pop_flash()
    response.headers[str('x-flash-messages')] = json.dumps(
        flash_messages)
