# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from ziggurat_foundations.models.group_permission import GroupPermissionMixin

from ziggurat_cms.models.meta import Base


class GroupPermission(GroupPermissionMixin, Base):
    pass
