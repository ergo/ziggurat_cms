from enum import Enum, unique


class NOOP(object):
    def __bool__(self):
        return False


noop = NOOP()


class BaseEnum(Enum):
    @classmethod
    def min(cls):
        min([x.value for x in cls])

    @classmethod
    def max(cls):
        max([x.value for x in cls])


@unique
class StatusEnum(BaseEnum):
    ACTIVE = 1
    DISABLED = 0
    DELETED = -1
    DRAFT = 2


@unique
class ResourceClassifiers(BaseEnum):
    NAVIGABLE = 1
    GRID_SUBELEMENT = 50
