# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sqlalchemy as sa
from ziggurat_foundations.models.services.resource import \
    ResourceService as Service


class ResourceService(Service):
    @classmethod
    def by_uuid(cls, uuid, tenant_pkey=None, db_session=None):
        query = db_session.query(cls.model).filter(
            cls.model.uuid == uuid)
        if tenant_pkey:
            query = query.filter(cls.model.tenant_pkey == tenant_pkey)
        return query.first()

    @classmethod
    def by_parent_id(cls, parent_id, db_session=None):
        query = db_session.query(cls.model).filter(
            cls.model.parent_id == parent_id)
        query = query.order_by(sa.asc(cls.model.ordering))
        return query

    @classmethod
    def check_element_classifiers(cls, request, instance, element_classifiers):
        definitions = request.registry.cms_resource_definitions
        node_definition = definitions[instance.resource_type]
        node_set = set(node_definition.get('element_classifiers') or [])
        elem_set = set(element_classifiers or [])
        if node_set.intersection(elem_set):
            return True
        return False
