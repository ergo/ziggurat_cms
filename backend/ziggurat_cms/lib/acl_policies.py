# -*- coding: utf-8 -*-

import logging

from pyramid.authentication import CallbackAuthenticationPolicy

from ziggurat_cms.lib import safe_uuid
from ziggurat_cms.services.auth_token import AuthTokenService

log = logging.getLogger(__name__)


class AuthTokenAuthenticationPolicy(CallbackAuthenticationPolicy):
    def __init__(self, callback=None):
        self.callback = callback

    def remember(self, request, principal, **kw):
        return []

    def forget(self, request):
        return []

    def unauthenticated_userid(self, request):
        token = u'{}'.format(
            request.headers.get('x-zigguratcms-auth-token', '')
        )
        if token:
            auth_token = AuthTokenService.by_token(
                safe_uuid(token), db_session=request.dbsession)
            if auth_token:
                log.info(
                    'AuthTokenAuthenticationPolicy.unauthenticated_userid',
                    extra={'found': True, 'owner': auth_token.owner_id})
                return auth_token.owner_id
            log.info('AuthTokenAuthenticationPolicy.unauthenticated_userid',
                     extra={'found': False, 'owner': None})

    def authenticated_userid(self, request):
        return self.unauthenticated_userid(request)
