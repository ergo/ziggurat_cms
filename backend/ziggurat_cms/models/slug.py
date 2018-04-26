# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import uuid

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from ziggurat_cms.models.meta import Base
from ziggurat_foundations.models.base import BaseModel


class Slug(BaseModel, Base):
    __tablename__ = 'slugs'

    pkey = sa.Column(sa.BigInteger(), primary_key=True)
    resource_id = sa.Column(sa.Integer(),
                            sa.ForeignKey('resources.resource_id',
                                          onupdate='CASCADE'))
    element_pkey = sa.Column(sa.Integer(),
                             sa.ForeignKey('node_elements.pkey',
                                           onupdate='CASCADE'))
    uuid = sa.Column(postgresql.UUID, default=lambda x: str(uuid.uuid4()),
                     nullable=False)
    text = sa.Column(sa.Unicode(512))
    counter = sa.Column(sa.Integer, default=1, nullable=False)
    tenant_pkey = sa.Column(sa.Integer)

    @property
    def prefixed_text(self):
        return '{}-{}'.format(self.counter, self.text)

    element = sa.orm.relationship(
        'NodeElement',
        passive_deletes=True,
        passive_updates=True,
        uselist=False)
