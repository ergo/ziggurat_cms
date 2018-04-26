# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from ziggurat_cms.models.node_element import NodeElement
from ziggurat_foundations.models.services import BaseService


class NodeElementService(BaseService):
    @classmethod
    def by_uuid(cls, uuid, db_session=None):
        return db_session.query(NodeElement).filter(
            NodeElement.uuid == uuid).first()
