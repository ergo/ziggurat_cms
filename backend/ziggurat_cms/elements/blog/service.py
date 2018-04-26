# -*- coding: utf-8 -*-
import logging

import sqlalchemy as sa
from paginate_sqlalchemy import SqlalchemyOrmPage
from ziggurat_cms.constants import StatusEnum
from ziggurat_cms.elements.blog.models.entry import ZigguratCMSBlogEntry
from ziggurat_cms.services.element_upload import ElementUploadImageBaseService
from ziggurat_foundations.models.services import BaseService

log = logging.getLogger(__name__)


class ElementUploadImageService(ElementUploadImageBaseService):
    pass


class ElementBlogService(BaseService):
    @classmethod
    def get_latest_entries(cls, instance, only_active=True, limit=20):
        query = instance.sub_elements
        query = query.order_by(sa.desc(ZigguratCMSBlogEntry.date_created))
        if only_active:
            query = query.filter(
                ZigguratCMSBlogEntry.status == StatusEnum.ACTIVE.value)
        if limit:
            query = query.limit(limit)
        return query

    @classmethod
    def get_paginator(cls, instance, page=1, item_count=None, items_per_page=50,
                      db_session=None,
                      filter_params=None, **kwargs):
        """ returns paginator over users belonging to the group"""
        if filter_params is None:
            filter_params = {}
        query = cls.get_latest_entries(instance, only_active=True, limit=None)
        return SqlalchemyOrmPage(query, page=page, item_count=item_count,
                                 items_per_page=items_per_page,
                                 **kwargs)


class ElementUploadImageService(ElementUploadImageBaseService):
    pass
