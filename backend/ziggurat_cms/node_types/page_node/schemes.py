from marshmallow import fields, Schema

from ziggurat_cms.validation.schemes import (
    ResourceCreateSchemaMixin,
    PageElementSchema)


class PageConfigSchema(Schema):
    pass


class PageNodeCreateSchema(ResourceCreateSchemaMixin):
    class Meta(object):
        strict = True
        ordered = True

    parent_uuid = fields.Str()
    description = fields.Str()
    config = fields.Nested(PageConfigSchema,
                           default=dict, missing=dict)


class PageNodeGETSchema(PageNodeCreateSchema):
    elements = fields.Nested(PageElementSchema, many=True,
                             attribute="listed_elements")


class PageNodeCreateAdminSchema(PageNodeCreateSchema):
    class Meta(object):
        strict = True
        ordered = True

    owner_user_id = fields.Int()
    owner_group_id = fields.Int()
    description = fields.Str()
    config = fields.Nested(PageConfigSchema,
                           default=dict, missing=dict)
