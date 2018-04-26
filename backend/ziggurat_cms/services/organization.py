# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from ziggurat_foundations.models.services import BaseService
from ziggurat_cms.models.organization import Organization

class OrganizationService(BaseService):
    def by_matched_domain(self, domain, db_session=None):
        db_session.query(Organization).filter(
            # Organization.
        )
