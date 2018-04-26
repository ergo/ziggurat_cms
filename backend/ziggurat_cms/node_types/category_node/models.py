# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from ziggurat_cms.models.resource import Resource


class CategoryNode(Resource):
    __mapper_args__ = {'polymorphic_identity': 'zigguratcms-category-node'}

    __possible_permissions__ = ['view', 'edit', 'delete']
