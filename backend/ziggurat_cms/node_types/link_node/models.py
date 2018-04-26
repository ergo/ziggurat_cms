# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from ziggurat_cms.models.resource import Resource


class LinkNode(Resource):
    __mapper_args__ = {'polymorphic_identity': 'zigguratcms-link-node'}

    __possible_permissions__ = ['view', 'edit', 'delete']
