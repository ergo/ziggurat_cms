# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from ziggurat_foundations.models.user_permission import UserPermissionMixin

from ziggurat_cms.models.meta import Base


class UserPermission(UserPermissionMixin, Base):
    pass
