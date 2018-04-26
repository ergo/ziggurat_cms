# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sqlalchemy as sa
from ziggurat_cms.models.meta import Base


class ApplicationDomain(Base):
    __tablename__ = 'applications_domains'

    resource_id = sa.Column('resource_id', sa.Integer(),
                            sa.ForeignKey('resources.resource_id',
                                          onupdate='CASCADE',
                                          ondelete='CASCADE', ),
                            primary_key=True)

    domain = sa.Column('domain', sa.Unicode(True), primary_key=True,
                       unique=True)
