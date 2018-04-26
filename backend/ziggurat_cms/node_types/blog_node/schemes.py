from marshmallow import fields, Schema

from ziggurat_cms.validation.schemes import (
    ResourceCreateSchemaMixin,
    PageElementSchema)


class BlogConfigSchema(Schema):
    pass


class BlogNodeCreateSchema(ResourceCreateSchemaMixin):
    class Meta(object):
        strict = True
        ordered = True

    parent_uuid = fields.Str()
    description = fields.Str()
    config = fields.Nested(BlogConfigSchema,
                           default=dict, missing=dict)

class BlogNodeGETSchema(BlogNodeCreateSchema):
    elements = fields.Nested(PageElementSchema, many=True,
                             attribute="listed_elements")


class BlogNodeCreateAdminSchema(BlogNodeCreateSchema):
    class Meta(object):
        strict = True
        ordered = True

    owner_user_id = fields.Int()
    owner_group_id = fields.Int()
    description = fields.Str()
    config = fields.Nested(BlogConfigSchema,
                           default=dict, missing=dict)
