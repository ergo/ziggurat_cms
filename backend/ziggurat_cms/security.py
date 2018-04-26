# -*- coding: utf-8 -*-

import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.security import Allow, Deny, ALL_PERMISSIONS, Authenticated, \
    Everyone
from ziggurat_foundations.permissions import permission_to_pyramid_acls

from ziggurat_cms.lib import safe_integer, safe_uuid
from ziggurat_cms.services.application import ApplicationService
from ziggurat_cms.services.node_element import NodeElementService
from ziggurat_cms.services.resource import ResourceService
from ziggurat_cms.services.slug import SlugService

log = logging.getLogger(__name__)


def groupfinder(userid, request):
    groups = ['group:__anonymous__']
    if userid and hasattr(request, 'user') and request.user:
        groups.extend(['group:%s' % g.id for g in request.user.groups])
        return groups
    return groups


class RootContext(object):
    pass


class ResourceContext(object):
    pass


class UsersContext(object):
    pass


def set_element_context(request, context,
                        element_uuid=None,
                        element_id=None,
                        element=None):
    """

    :param request:
    :param context:
    :param element_uuid:
    :param element_id:
    :param element:
    :return:
    """
    if element:
        context.element = element
    elif element_id:
        context.element = NodeElementService.get(
            element_uuid, db_session=request.dbsession)
    else:
        r_uuid = request.matchdict.get("uuid")
        r_uuid = safe_uuid(r_uuid) if r_uuid else None
        element_uuid = element_uuid or r_uuid
        context.element = NodeElementService.by_uuid(
            element_uuid, db_session=request.dbsession)
    if not context.element:
        raise HTTPNotFound()

    context.resource = context.element.resource

    extend_acl_from_resource(request, context=context,
                             resource=context.resource)


def rewrite_admin_perm(outcome, perm_user, perm_name,
                       to_rewrite='root_administration'):
    """
    Translates root_administration into ALL_PERMISSIONS object
    """
    if perm_name == to_rewrite:
        return outcome, perm_user, ALL_PERMISSIONS
    else:
        return outcome, perm_user, perm_name


def allow_root_access(request, context):
    """
    Adds ALL_PERMISSIONS to every resource if user has 'root_administration' permission
    """
    if getattr(request, 'user'):
        for perm in permission_to_pyramid_acls(request.user.permissions):
            if perm[2] == 'root_administration':
                context.__acl__.append(
                    (perm[0], perm[1], ALL_PERMISSIONS))


def allow_admin_access(request, context):
    """
    Adds ALL_PERMISSIONS to every resource if user has 'administration',
    EXCLUDING ROOT PERMISSION
    """
    if getattr(request, 'user'):
        for perm in permission_to_pyramid_acls(request.user.permissions):
            if perm[2] == 'administration':
                context.__acl__.append(
                    (Deny, perm[1], 'root_administration'))
                context.__acl__.append(
                    (perm[0], perm[1], ALL_PERMISSIONS))


def api_resources_security_factory(request, **kwargs):
    """
    Default security factory for resource nodes
    :param request:
    :return:
    """
    non_id_routes = ['objects', 'api_objects']
    is_base_object_route = request.matched_route and \
                           request.matched_route.name in non_id_routes
    context = ResourceContext()
    set_base_context_info(request, context)
    # find resource from uuid or use top-level app if base object route
    root_resource = context.application if is_base_object_route else None
    set_resource_context(request, context=context, resource=root_resource)
    return context


def api_users_security_factory(request, **kwargs):
    """
    Returns user context from uuid
    :param request:
    :return:
    """
    context = UsersContext()
    set_base_context_info(request, context)
    allow_root_access(request, context=context)
    allow_admin_access(request, context=context)
    # user can see itself
    if request.matchdict.get('uuid') == 'self':
        context.__acl__.append((Allow, request.user.id, 'view_self_api'))
    return context


def static_factory(request, **kwargs):
    """
    Currently does nothing for static resources
    :param request:
    :return:
    """
    pass


def root_factory(request, **kwargs):
    """
    Returns RootContext with tenant information
    :param request:
    :return:
    """
    context = RootContext()
    set_base_context_info(request, context)
    return context


def index_factory(request, **kwargs):
    """
    Returns RootContext with tenant information
    :param request:
    :return:
    """
    context = RootContext()
    set_base_context_info(request, context)
    resource_context_mappings = request.registry.zigg_resource_context_mappings
    index_node_uuid = context.application.config.get('index_node_uuid', None)
    resource = None
    if index_node_uuid:
        resource = ResourceService.by_uuid(
            index_node_uuid, tenant_pkey=context.application.resource_id,
            db_session=request.dbsession)

    if not resource:
        resource = context.application.children.first()
    if resource and resource.resource_type in resource_context_mappings:
        return resource_context_mappings[resource.resource_type](
            request, slug=None, resource=resource)

    raise HTTPFound(location=request.route_path('admin_index', partial=''))


def security_factory_selector(request):
    """
    Tries to pick proper context factory based on object type
    :param request:
    :return:
    """
    registry = request.registry
    security_factories_keys = registry.zigg_context_factories.keys()
    object_type = request.matchdict['object']
    for key in security_factories_keys:
        if object_type.startswith(key):
            factory = registry.zigg_context_factories.get(key)
            log.debug('factory selected:{} object_type:{}'.format(
                factory, object_type
            ))
            if factory:
                return factory(request)
            break
    return root_factory(request)


def slug_security_factory(request, **kwargs):
    """
    Tries to return proper element context from slug
    :param request:
    :return:
    """
    context = RootContext()
    set_base_context_info(request, context)

    try:
        counter, slug_text = request.matchdict['slug'].split('-', 1)
    except ValueError:
        raise HTTPNotFound()

    slug = SlugService.by_slug(
        context.application.resource_id,
        slug_text,
        safe_integer(counter),
        db_session=request.dbsession)
    if not slug:
        return None
    element = slug.element
    resource = slug.resource
    element_context_mappings = request.registry.zigg_element_context_mappings
    resource_context_mappings = request.registry.zigg_resource_context_mappings
    # elements use their own mappings
    if element and element.type in element_context_mappings:
        return element_context_mappings[element.type](
            request, slug=slug)
    # nodes can define their mappings too
    elif resource.resource_type in resource_context_mappings:
        return resource_context_mappings[resource.resource_type](
            request, slug=slug, resource=slug.resource)
    # if everything else fails try to return root context
    else:
        set_resource_context(request, context=context, resource=resource)
        return context


def filter_admin_panel_perms(item):
    if str(item[2]).startswith('admin_'):
        return False
    return True


def extend_acl_from_resource(request, context, resource):
    context.__acl__.extend(resource.__acl__)
    if request.user:
        # add perms that this user has for this resource
        # this is a big performance optimization - we fetch only data
        # needed to check one specific user
        permissions = ResourceService.perms_for_user(resource, request.user)
        for outcome, perm_user, perm_name in permission_to_pyramid_acls(
                permissions):
            context.__acl__.append(
                rewrite_admin_perm(outcome, perm_user, perm_name,
                                   to_rewrite='administration'))
    allow_root_access(request, context=context)
    allow_admin_access(request, context=context)


def set_base_context_info(request, context):
    """
    Populates tenant and application info + default ACL
    :param request:
    :param context:
    :return:
    """
    context.__acl__ = [(Allow, Authenticated, 'authenticated')]
    # view perm for everyone for debug purposes
    context.__acl__.append((Allow, Everyone, 'view'))

    context.organization = None
    context.application = None
    domains = [request.domain, '*.{}'.format(request.domain)]
    results = ApplicationService.by_matched_domains(
        domains=domains, db_session=request.dbsession)
    context.application = results.first()
    if context.application:
        context.organization = ResourceService.get(
            context.application.resource_id, db_session=request.dbsession)
    if not context.application:
        log.warning('security.application_not_found', extra={
            'domains': domains
        })
        raise HTTPNotFound()


def set_resource_context(request, context, resource=None):
    if resource:
        context.resource = resource
    else:
        uuid_id = request.matchdict.get("uuid")
        context.resource = ResourceService.by_uuid(
            uuid_id, db_session=request.dbsession)
    if not context.resource:
        raise HTTPNotFound()

    extend_acl_from_resource(request, context=context,
                             resource=context.resource)


def set_default_context_factories(config):
    log.debug('setting default context factories')
    config.registry.zigg_context_factories = {
        'applications': api_resources_security_factory,
        'resources': api_resources_security_factory,
        'users': api_users_security_factory
    }
    config.registry.zigg_element_context_mappings = {}
    config.registry.zigg_resource_context_mappings = {}
