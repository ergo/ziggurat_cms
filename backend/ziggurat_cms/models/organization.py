# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sqlalchemy as sa

from ziggurat_cms.models.resource import Resource


class Organization(Resource):
    """
    Resource of application type
    """

    __tablename__ = 'organizations'
    __mapper_args__ = {'polymorphic_identity': 'organization'}

    __possible_permissions__ = ['view', 'edit']

    resource_id = sa.Column(sa.Integer(),
                            sa.ForeignKey('resources.resource_id',
                                          onupdate='CASCADE',
                                          ondelete='CASCADE', ),
                            primary_key=True)
