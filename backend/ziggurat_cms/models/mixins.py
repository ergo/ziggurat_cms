from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr


class ModifiedTimesMixin(object):
    @declared_attr
    def date_created(self):
        return sa.Column(sa.DateTime(), default=datetime.utcnow)

    @declared_attr
    def date_modified(self):
        return sa.Column(sa.DateTime(), default=datetime.utcnow)

    @declared_attr
    def date_deleted(self):
        return sa.Column(sa.DateTime())
