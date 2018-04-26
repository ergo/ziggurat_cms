# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import uuid

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from ziggurat_foundations.models.base import BaseModel

from ziggurat_cms.models.meta import Base


class AuthToken(BaseModel, Base):
    """
    Auth tokens that can be used to authenticate as specific users
    """
    __tablename__ = 'auth_tokens'

    pkey = sa.Column(sa.Integer, primary_key=True, nullable=False)
    uuid = sa.Column(postgresql.UUID, nullable=False,
                     default=lambda: str(uuid.uuid4()))
    token = sa.Column(postgresql.UUID, nullable=False,
                      default=lambda: str(uuid.uuid4()))
    owner_id = sa.Column(sa.Integer,
                         sa.ForeignKey('users.id', onupdate='CASCADE',
                                       ondelete='CASCADE'))
