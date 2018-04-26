# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import json
import logging
from datetime import datetime

from authomatic.adapters import WebObAdapter
from pyramid.httpexceptions import HTTPFound
from pyramid.i18n import TranslationStringFactory
from pyramid.response import Response
from pyramid.security import NO_PERMISSION_REQUIRED, remember, forget
from pyramid.view import view_config
from ziggurat_cms.events import SocialAuthEvent
from ziggurat_cms.services.user import UserService
from ziggurat_cms.views import BaseView
from ziggurat_foundations.models.services.external_identity import \
    ExternalIdentityService

log = logging.getLogger(__name__)

_ = TranslationStringFactory('ziggurat_cms')


class AuthView(BaseView):
    @view_config(route_name='sign_in', permission=NO_PERMISSION_REQUIRED)
    def sign_in(self):
        came_from = self.request.params.get('came_from', '/')
        user_name = self.request.params.get('login', '')
        password = self.request.params.get('password', '')
        resource_id = self.request.context.application.resource_id
        user = UserService.by_prefixed_user_name(
            user_name, tenant_pkey=resource_id, db_session=self.request.dbsession)
        if user is None:
            # if no result, test to see if email exists
            user = UserService.by_prefixed_email(
                user_name, tenant_pkey=resource_id, db_session=self.request.dbsession)
        if user:
            if user.check_password(password):
                headers = remember(self.request, user.id)
                return self.sign_in_success(user, headers, came_from)
        headers = forget(self.request)
        return self.sign_in_bad_auth(headers, came_from)

    @view_config(route_name='sign_out', permission=NO_PERMISSION_REQUIRED)
    def sign_out(self):
        headers = forget(self.request)
        return self.sign_out_success(headers)

    def sign_in_success(self, user, headers, came_from):
        user.last_login_date = datetime.utcnow()
        return self.shared_sign_in(user, headers, came_from)

    def sign_in_bad_auth(self, headers, came_from):
        request = self.request
        log.info('bad_auth', {'user': None})
        # action like a warning flash message on bad logon
        msg = {'msg': self.translate(_('Wrong username or password')),
               'level': 'danger'}
        request.session.flash(msg)
        if request.headers.get('accept') == 'application/json':
            response = Response()
            response.status_code = 401
            return response
        request.keep_flash = True
        return HTTPFound(location=request.route_url('register'),
                         headers=headers)

    def sign_out_success(self, headers):
        request = self.request
        request.session.flash(
            {'msg': self.translate(_('Signed out')), 'level': 'success'})
        request.keep_flash = True
        return HTTPFound(location=request.route_url('/'), headers=headers)

    @view_config(route_name='social_auth', permission=NO_PERMISSION_REQUIRED)
    def social_auth(self):
        request = self.request
        # Get the internal provider name URL variable.
        provider_name = request.matchdict.get('provider')

        # Start the login procedure.
        adapter = WebObAdapter(request, request.response)
        result = request.authomatic.login(adapter, provider_name)
        if result:
            if result.error:
                return self.handle_auth_error(result)
            elif result.user:
                return self.handle_auth_success(result)
        request.keep_flash = True
        return request.response

    def handle_auth_error(self, result):
        request = self.request
        # Login procedure finished with an error.
        request.session.pop('zigg.social_auth', None)
        log.error('social_auth', extra={'error': result.error.message})
        msg = {'msg': self.translate(
            _('Something went wrong when accessing third party '
              'provider - please try again')),
            'level': 'danger'}
        request.session.flash(msg)
        request.keep_flash = True
        return HTTPFound(location=request.route_url('/'))

    def handle_auth_success(self, result):
        request = self.request
        # Hooray, we have the user!
        # OAuth 2.0 and OAuth 1.0a provide only limited user data on login,
        # We need to update the user to get more info.
        if result.user:
            result.user.update()
        social_data = {
            'user': {'data': result.user.data},
            'credentials': result.user.credentials
        }
        # normalize data
        social_data['user']['id'] = result.user.id
        user_name = result.user.username or ''
        # use email name as username for google
        if (social_data['credentials'].provider_name == 'google' and
                result.user.email):
            user_name = result.user.email
        social_data['user']['user_name'] = user_name
        social_data['user']['email'] = result.user.email or ''

        request.session['zigg.social_auth'] = social_data
        # user is logged so bind his external identity with account
        if request.user:
            log.info('social_auth', extra={'user_found': True})
            request.registry.notify(SocialAuthEvent(request, request.user,
                                                    social_data))
            request.session.pop('zigg.social_auth', None)
            http_response = HTTPFound(location=request.route_url('/'))
        else:
            log.info('social_auth', extra={'user_found': False})

            user = ExternalIdentityService.user_by_external_id_and_provider(
                social_data['user']['id'],
                social_data['credentials'].provider_name,
                db_session=request.dbsession
            )
            # user tokens are already found in our db
            if user:
                request.registry.notify(SocialAuthEvent(request, user,
                                                        social_data))
                headers = remember(request, user.id)
                request.session.pop('zigg.social_auth', None)
                http_response = self.shared_sign_in(user, headers)
            else:
                msg = {'msg': self.translate(
                    _('You need to finish registration '
                      'process to bind your external '
                      'identity to your account or sign in to '
                      'existing account')),
                    'level': 'warning'}
                request.session.flash(msg)
                http_response = HTTPFound(
                    location=request.route_url('register'))
        # handle ajax logins - for example admin panel
        if request.headers.get('accept') == 'application/json':
            response = Response()
            return response
        request.keep_flash = True
        return http_response

    def shared_sign_in(self, user, headers, came_from=None):
        """ Shared among sign_in and social_auth views"""
        request = self.request
        # actions performed on sucessful logon, flash message/new csrf token
        # user status validation etc.
        if came_from is None:
            came_from = request.route_url('/')

        log.info('shared_sign_in', extra={'user': user})
        request.session.flash(
            {'msg': self.translate(_('Signed in')), 'level': 'success'})
        # if social data is still present bind the account
        social_data = request.session.get('zigg.social_auth')
        if social_data:
            request.registry.notify(SocialAuthEvent(request, user, social_data))
            request.session.pop('zigg.social_auth', None)

        if request.headers.get('accept') == 'application/json':
            response = Response(json.dumps({'uuid': str(user.uuid)}),
                                headers=headers)
            # add clobbered x-user-uuid header
            response.headers[str('x-user-uuid')] = str(user.uuid)
            return response
        request.keep_flash = True
        return HTTPFound(location=came_from, headers=headers)
