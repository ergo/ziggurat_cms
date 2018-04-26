# -*- coding: utf-8 -*-

import datetime
import json
import os
import warnings

from pkg_resources import iter_entry_points
import ziggurat_cms.lib.cache_regions as cache_regions
import ziggurat_cms.lib.encryption as encryption
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator, PHASE3_CONFIG
from pyramid.renderers import JSON
from pyramid.security import AllPermissionsList
from pyramid_authstack import AuthenticationStackPolicy
from ziggurat_cms.celery import configure_celery
from ziggurat_cms.security import groupfinder, set_default_context_factories
from ziggurat_cms.lib.acl_policies import AuthTokenAuthenticationPolicy
from ziggurat_cms.services.element_upload import ElementUploadBaseService


def gen_directories(config):
    settings = config.registry.settings
    ElementUploadBaseService.gen_directory(
        settings['static.dir'], '')
    ElementUploadBaseService.gen_directory(
        settings['static.build_dir'], '')
    ElementUploadBaseService.gen_directory(
        settings['upload.root_dir'], '')
    ElementUploadBaseService.gen_directory(
        settings['upload.root_dir'], 'public')
    ElementUploadBaseService.gen_directory(
        settings['upload.root_dir'], 'private')


def normalize_settings(config):
    settings = config.registry.settings
    settings['upload.root_dir'] = os.path.abspath(settings['upload.root_dir'])
    settings['static.dir'] = os.path.abspath(settings['static.dir'])


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    settings.setdefault('jinja2.i18n.domain', 'ziggurat_cms')

    stacked_policy = AuthenticationStackPolicy()
    auth_tkt = AuthTktAuthenticationPolicy(settings['auth_tkt.seed'],
                                           callback=groupfinder)
    auth_token_policy = AuthTokenAuthenticationPolicy(callback=groupfinder)

    stacked_policy.add_policy('auth_tkt', auth_tkt)
    stacked_policy.add_policy('auth_token', auth_token_policy)
    authorization_policy = ACLAuthorizationPolicy()

    settings['jinja2.undefined'] = 'strict'
    config = Configurator(settings=settings,
                          authentication_policy=stacked_policy,
                          authorization_policy=authorization_policy,
                          root_factory='ziggurat_cms.security.root_factory',
                          default_permission='view')
    config.add_translation_dirs('ziggurat_cms:locale/',
                                'wtforms:locale/', )

    # modify json renderer
    json_renderer = JSON(indent=4)

    def datetime_adapter(obj, request):
        return obj.isoformat()

    def all_permissions_adapter(obj, request):
        return '__all_permissions__'

    json_renderer.add_adapter(datetime.datetime, datetime_adapter)
    json_renderer.add_adapter(datetime.date, datetime_adapter)
    json_renderer.add_adapter(AllPermissionsList, all_permissions_adapter)
    config.add_renderer('json', json_renderer)

    # set crypto key used to store sensitive data like auth tokens
    encryption.ENCRYPTION_SECRET = settings['encryption_secret']
    # CSRF is enabled by defualt
    # use X-XSRF-TOKEN for angular

    def csrf_callback(request):
        return 'auth:auth_token' not in request.effective_principals

    config.set_default_csrf_options(require_csrf=True, header='X-XSRF-TOKEN',
                                    callback=csrf_callback)

    config.include('pyramid_mailer')
    config.include('pyramid_jinja2')
    config.include('pyramid_redis_sessions')
    normalize_settings(config)
    gen_directories(config)
    set_default_context_factories(config)

    # make request.user available
    config.add_request_method(
        'ziggurat_cms.lib.request:keep_flash', 'keep_flash', reify=True)
    config.add_request_method(
        'ziggurat_cms.lib.request:get_user', 'user', reify=True)
    config.add_request_method(
        'ziggurat_cms.lib.request:safe_json_body', 'safe_json_body',
        reify=True)
    config.add_request_method(
        'ziggurat_cms.lib.request:unsafe_json_body', 'unsafe_json_body',
        reify=True)
    config.add_request_method(
        'ziggurat_cms.lib.request:get_authomatic', 'authomatic',
        reify=True)
    config.add_request_method('ziggurat_cms.lib.request.handle_cors',
                              'handle_cors')


    config.add_directive(
        'cms_register_resource',
        'ziggurat_cms.lib.configurator.cms_register_resource')

    config.add_directive(
        'cms_register_node_element',
        'ziggurat_cms.lib.configurator.cms_register_node_element')

    config.add_directive(
        'cms_register_frontend_asset',
        'ziggurat_cms.lib.configurator.cms_register_frontend_asset')

    # config.add_view_deriver(
    #     'ziggurat_cms.view_derivers.dynamic_template_deriver',
    #     under='rendered_view', over='mapped_view')

    config.scan('ziggurat_cms.events')
    config.scan('ziggurat_cms.subscribers')
    config.include('ziggurat_cms.models')
    config.include('ziggurat_cms.routes')
    config.include('ziggurat_cms.views')
    config.include('ziggurat_cms.node_types')
    config.include('ziggurat_cms.elements')

    def pre_commit():
        jinja_env = config.get_jinja2_environment()
        jinja_env.filters['tojson'] = json.dumps

    config.action(None, pre_commit, order=PHASE3_CONFIG + 999)

    # configure celery in later phase
    def wrap_config_celery():
        configure_celery(config.registry)

    config.action(None, wrap_config_celery, order=PHASE3_CONFIG + 999)

    # setup dogpile cache
    config.registry.cache_regions = cache_regions.CacheRegions(settings)

    for entry_point in iter_entry_points(group='ziggurat_cms.packages'):
        plugin = entry_point.load()
        plugin.includeme(config)

    if not config.registry.settings.get('ziggurat_cms.ignore_warnings', True):
        warnings.filterwarnings('default')
    return config.make_wsgi_app()
