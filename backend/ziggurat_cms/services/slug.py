# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

import sqlalchemy as sa
from ziggurat_cms.lib import generate_slug_text
from ziggurat_cms.models.slug import Slug
from ziggurat_foundations.models.services import BaseService

log = logging.getLogger(__name__)


class SlugService(BaseService):
    @classmethod
    def create_slug(cls, tenant_pkey, resource_id, text, element_pkey=None,
                    db_session=None):
        slug_text = generate_slug_text(text)

        slug = SlugService.by_slug(tenant_pkey, slug_text,
                                   db_session=db_session)
        counter = 1
        if slug and slug.resource_id == resource_id and \
                        slug.element_pkey == element_pkey:
            return slug
        if slug:
            counter += slug.counter

        new_slug = Slug(
            tenant_pkey=tenant_pkey, text=slug_text, counter=counter,
            resource_id=resource_id, element_pkey=element_pkey)
        new_slug.persist(flush=True, db_session=db_session)
        return new_slug

    @classmethod
    def by_text(cls, tenant_pkey, text, db_session=None):
        slug_text = generate_slug_text(text)
        return cls.by_slug(tenant_pkey, slug_text=slug_text,
                           db_session=db_session)

    @classmethod
    def by_slug(cls, tenant_pkey, slug_text, counter=None, db_session=None):
        query = db_session.query(Slug)
        query = query.filter(Slug.text == slug_text)
        query = query.filter(Slug.tenant_pkey == tenant_pkey)
        if counter:
            query = query.filter(Slug.counter == counter)
        return query.order_by(sa.desc(Slug.counter)).first()
