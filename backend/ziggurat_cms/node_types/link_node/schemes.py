from marshmallow import fields, Schema

from ziggurat_cms.validation.schemes import (
    ResourceCreateSchemaMixin)


class LinkConfigSchema(Schema):
    link = fields.String(default='', missing='')


class LinkNodeCreateSchema(ResourceCreateSchemaMixin):
    class Meta(object):
        strict = True
        ordered = True

    parent_uuid = fields.Str()
    description = fields.Str()
    config = fields.Nested(LinkConfigSchema,
                           default=dict, missing=dict)


class LinkNodeCreateAdminSchema(LinkNodeCreateSchema):
    class Meta(object):
        strict = True
        ordered = True

    owner_user_id = fields.Int()
    owner_group_id = fields.Int()
    description = fields.Str()
    config = fields.Nested(LinkConfigSchema,
                           default=dict, missing=dict)
