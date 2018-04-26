from marshmallow import (fields, validate)
from ziggurat_cms.validation.schemes import PageElementSchema


class BlogEntrySchema(PageElementSchema):
    name = fields.Str(validate=(validate.Length(min=1, max=256)))

    tag = fields.List(fields.String(validate=(validate.Length(min=1, max=100))))

    date_created = fields.DateTime()
