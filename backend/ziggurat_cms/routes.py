# -*- coding: utf-8 -*-
import os

from pyramid.security import NO_PERMISSION_REQUIRED


def includeme(config):
    # , cache_max_age=3600
    config.add_static_view('static', 'static', cache_max_age=1,
                           permission=NO_PERMISSION_REQUIRED,
                           factory='ziggurat_cms.security.static_factory')
    config.override_asset(
        to_override='ziggurat_cms:static/',
        override_with=config.registry.settings['static.dir'])

    config.add_static_view('uploads', 'uploads', cache_max_age=1,
                           permission=NO_PERMISSION_REQUIRED,
                           factory='ziggurat_cms.security.static_factory')
    public_path = os.path.join(config.registry.settings['upload.root_dir'],
                               'public')
    config.override_asset(
        to_override='ziggurat_cms:uploads/public/',
        override_with=public_path)
    config.add_route('CORS_route', '*foo', request_method='OPTIONS')
    config.add_route('/', '/', factory='ziggurat_cms.security.index_factory',
                     use_global_views=True)
    config.add_route('sign_in', '/sign_in')
    config.add_route('sign_out', '/sign_out')
    config.add_route('admin_index', '/admin*partial')
    config.add_route('register', '/register')
    config.add_route('lost_password', '/lost_password')
    config.add_route('lost_password_generate', '/lost_password_generate')
    config.add_route('social_auth', '/social_auth/{provider}')

    config.add_route('object_slug', '/o/{slug}',
                     factory='ziggurat_cms.security.slug_security_factory')
    config.add_route('element_slug', '/e/{slug}',
                     factory='ziggurat_cms.security.slug_security_factory')
    config.add_route('element_slug_action', '/e/{slug}/verb/{verb}',
                     factory='ziggurat_cms.security.slug_security_factory')
    config.add_route('objects', '/o/{object}/verb/{verb}',
                     factory='ziggurat_cms.security.security_factory_selector')
    config.add_route('object', '/o/{object}/{uuid}/verb/{verb}',
                     factory='ziggurat_cms.security.security_factory_selector')
    config.add_route('object_relation',
                     '/o/{object}/{uuid}/{relation}/verb/{verb}',
                     factory='ziggurat_cms.security.security_factory_selector')

    config.add_route('element', '/e/{object}/{uuid}',
                     factory='ziggurat_cms.security.security_factory_selector')
    config.add_route('element_relation', '/e/{object}/{uuid}/rel/{relation}',
                     factory='ziggurat_cms.security.security_factory_selector')
    config.add_route('api_objects', '/api/{version}/{object}',
                     factory='ziggurat_cms.security.security_factory_selector')
    config.add_route('api_object_relation',
                     '/api/{version}/{object}/{uuid}/rel/{relation}',
                     factory='ziggurat_cms.security.security_factory_selector')
    config.add_route('api_object', '/api/{version}/{object}/{uuid}*remainder',
                     factory='ziggurat_cms.security.security_factory_selector')

    config.add_route('sitemap_xml', '/sitemap.xml')
