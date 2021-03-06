# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from ziggurat_foundations.models.external_identity import ExternalIdentityMixin

from ziggurat_cms.models.meta import Base
from ziggurat_cms.lib.sqlalchemy import EncryptedUnicode


class ExternalIdentity(ExternalIdentityMixin, Base):
    @declared_attr
    def access_token(self):
        return sa.Column(EncryptedUnicode(255), default='')

    @declared_attr
    def alt_token(self):
        return sa.Column(EncryptedUnicode(255), default='')

    @declared_attr
    def token_secret(self):
        return sa.Column(EncryptedUnicode(255), default='')
