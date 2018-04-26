from marshmallow import fields, Schema

from ziggurat_cms.validation.schemes import (
    ResourceCreateSchemaMixin)


class CategoryConfigSchema(Schema):
    list_children = fields.Boolean(default=False, missing=False)


class CategoryNodeCreateSchema(ResourceCreateSchemaMixin):
    class Meta(object):
        strict = True
        ordered = True

    parent_uuid = fields.Str()
    description = fields.Str()
    config = fields.Nested(CategoryConfigSchema,
                           default=dict, missing=dict)


class CategoryNodeCreateAdminSchema(CategoryNodeCreateSchema):
    class Meta(object):
        strict = True
        ordered = True

    owner_user_id = fields.Int()
    owner_group_id = fields.Int()
    description = fields.Str()
    config = fields.Nested(CategoryConfigSchema,
                           default=dict, missing=dict)
