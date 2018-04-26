# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from ziggurat_foundations.models.user_group import UserGroupMixin

from ziggurat_cms.models.meta import Base


class UserGroup(UserGroupMixin, Base):
    pass
