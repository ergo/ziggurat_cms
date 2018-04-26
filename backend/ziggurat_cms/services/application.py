# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from ziggurat_foundations.models.services import BaseService

from ziggurat_cms.models.application import Application
from ziggurat_cms.models.application_domain import ApplicationDomain
from ziggurat_cms.models.resource import Resource
from ziggurat_cms.validation.schemes import ApplicationNodeConfigSchema


class ApplicationService(BaseService):
    @classmethod
    def by_matched_domains(cls, domains, db_session=None):
        query = db_session.query(Resource).with_polymorphic([Application])
        query = query.filter(
            Resource.resource_id == ApplicationDomain.resource_id)
        query = query.filter(ApplicationDomain.domain.in_(domains))
        return query

    @classmethod
    def set_defaults(cls, instance):
        schema = ApplicationNodeConfigSchema()
        instance.config = schema.load({}).data

    @classmethod
    def get_title(cls, instance):
        return instance.config['http_title'] or instance.resource_name
