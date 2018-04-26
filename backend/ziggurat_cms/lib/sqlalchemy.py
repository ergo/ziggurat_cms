# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sqlalchemy.types as types
import ziggurat_cms.lib.encryption as encryption
from sqlalchemy.ext.mutable import Mutable


class EncryptedUnicode(types.TypeDecorator):
    impl = types.Unicode

    def process_bind_param(self, value, dialect):
        if not value:
            return value
        return encryption.encrypt_fernet(value.encode('utf8'))

    def process_result_value(self, value, dialect):
        if not value:
            return value
        return encryption.decrypt_fernet(value).decode('utf8')


class MutableDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        """Convert plain dictionaries to MutableDict."""

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        """Detect dictionary set events and emit change events."""

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        """Detect dictionary del events and emit change events."""

        dict.__delitem__(self, key)
        self.changed()
