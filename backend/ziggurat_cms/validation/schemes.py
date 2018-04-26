# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from marshmallow import (Schema, fields, validate, validates, validates_schema)
from pyramid.i18n import TranslationStringFactory
from ziggurat_foundations import noop
from ziggurat_foundations.exc import (
    ZigguratResourceOutOfBoundaryException,
    ZigguratResourceTreeMissingException,
    ZigguratResourceTreePathException
)

from ziggurat_cms import constants
from ziggurat_cms.services.group import GroupService
from ziggurat_cms.services.resource import ResourceService
from ziggurat_cms.services.resource_tree_service import tree_service
from ziggurat_cms.services.user import UserService

_ = TranslationStringFactory('ziggurat_cms')

user_regex_error = _('Username can only consist of '
                     'alphanumerical characters, hypens and underscores')


class UserCreateSchema(Schema):
    class Meta(object):
        strict = True
        ordered = True

    id = fields.Int(dump_only=True)
    uuid = fields.Str(dump_only=True)
    public_user_name = fields.Str(required=True,
                                  validate=(validate.Length(3),
                                            validate.Regexp('^[\w-]*$',
                                                            error=user_regex_error)))
    password = fields.Str(required=True, validate=(validate.Length(3)))
    public_email = fields.Str(required=True,
                              validate=(
                                  validate.Email(error=_('Not a valid email'))))
    status = fields.Int(dump_only=True)
    last_login_date = fields.DateTime(dump_only=True)
    registered_date = fields.DateTime(dump_only=True)

    @validates('public_user_name')
    def validate_user_name(self, value):
        request = self.context['request']
        modified_obj = self.context.get('modified_obj')
        user = UserService.by_prefixed_user_name(
            request.context.application.resource_id,
            value, db_session=request.dbsession)
        by_admin = request.has_permission('root_administration')
        if modified_obj and not by_admin and (modified_obj.user_name != value):
            msg = _('Only administrator can change usernames')
            raise validate.ValidationError(msg)
        if user:
            if not modified_obj or modified_obj.id != user.id:
                msg = _('User already exists in database')
                raise validate.ValidationError(msg)

    @validates('public_email')
    def validate_email(self, value):
        request = self.context['request']
        modified_obj = self.context.get('modified_obj')
        user = UserService.by_prefixed_email(
            request.context.application.resource_id,
            value, db_session=request.dbsession)
        if user:
            if not modified_obj or modified_obj.id != user.id:
                msg = _('Email already exists in database')
                raise validate.ValidationError(msg)


class UserEditSchema(UserCreateSchema):
    public_user_name = fields.Str(dump_only=True)
    password = fields.Str(required=False, validate=(validate.Length(3)))


class UserSearchSchema(Schema):
    class Meta(object):
        strict = True
        ordered = True

    public_user_name = fields.Str()
    public_user_name_like = fields.Str()

    # @pre_load()
    # def make_object(self, data):
    #     return list(data)


class GroupEditSchema(Schema):
    class Meta(object):
        strict = True
        ordered = True

    id = fields.Int(dump_only=True)
    member_count = fields.Int(dump_only=True)
    group_name = fields.Str(required=True,
                            validate=(validate.Length(3)))
    description = fields.Str()

    @validates('group_name')
    def validate_group_name(self, value):
        request = self.context['request']
        modified_obj = self.context.get('modified_obj')
        group = GroupService.by_group_name(value, db_session=request.dbsession)
        if group:
            if not modified_obj or modified_obj.id != group.id:
                msg = _('Group already exists in database')
                raise validate.ValidationError(msg)


class ResourceCreateSchemaMixin(Schema):
    class Meta(object):
        strict = True
        ordered = True

    uuid = fields.Str(dump_only=True)
    resource_type = fields.Str(dump_only=True)
    parent_uuid = fields.Str(validate=(validate.Length(
        min=1, max=100)))
    resource_name = fields.Str(required=True, validate=(validate.Length(
        min=1, max=100)))
    status = fields.Int(
        default=constants.StatusEnum.ACTIVE.value,
        validate=(validate.Range(min=constants.StatusEnum.ACTIVE.min(),
                                 max=constants.StatusEnum.ACTIVE.max())))
    ordering = fields.Int()
    depth = fields.Int(dump_only=True)
    owner_user_id = fields.Int(dump_only=True)
    owner_group_id = fields.Int(dump_only=True)
    config = fields.Raw()
    config_schema_version = fields.Integer(dump_only=True)

    @validates('parent_uuid')
    def validate_parent_uuid(self, value):
        request = self.context['request']
        resource = self.context.get('modified_obj')
        new_parent_uuid = value
        if not new_parent_uuid:
            return True
        resource_id = resource.resource_id if resource else None
        if new_parent_uuid is None:
            return True

        try:
            node = ResourceService.by_uuid(
                new_parent_uuid, db_session=request.dbsession)
            if not node:
                raise (ZigguratResourceTreeMissingException(
                    _('New parent node not found')))
            new_parent_id = node.resource_id
            tree_service.check_node_parent(
                resource_id, new_parent_id, db_session=request.dbsession)
        except ZigguratResourceTreeMissingException as exc:
            raise validate.ValidationError(str(exc))
        except ZigguratResourceTreePathException as exc:
            raise validate.ValidationError(str(exc))

    @validates_schema
    def validate_ordering(self, data):
        request = self.context['request']
        resource = self.context.get('modified_obj')
        new_parent_uuid = data.get('parent_uuid') or noop
        to_position = data.get('ordering')
        if to_position is None or to_position == 1:
            return

        same_branch = False

        # reset if parent is same as old
        if resource and new_parent_uuid == resource.parent_uuid:
            new_parent_uuid = noop

        if new_parent_uuid is noop and resource:
            same_branch = True

        parent_id = None

        if resource:
            if new_parent_uuid is noop:
                parent_id = resource.parent_id
            else:
                parent_id = ResourceService.by_uuid(
                    new_parent_uuid, db_session=request.dbsession).resource_id
        else:
            if new_parent_uuid is not noop:
                parent_id = ResourceService.by_uuid(
                    new_parent_uuid, db_session=request.dbsession).resource_id
        try:
            tree_service.check_node_position(
                parent_id, to_position, on_same_branch=same_branch,
                db_session=request.dbsession)
        except ZigguratResourceOutOfBoundaryException as exc:
            raise validate.ValidationError(str(exc), 'ordering')


class ResourceCreateSchema(ResourceCreateSchemaMixin):
    pass


class PageElementSchema(Schema):
    class Meta(object):
        strict = True
        ordered = True

    uuid = fields.Str(dump_only=True)
    type = fields.Str(required=True, validate=(validate.Length(min=1, max=64)))
    resource_id = fields.Integer(dump_only=True)
    parent_element_pkey = fields.Integer(dump_only=True)
    status = fields.Int(default=constants.StatusEnum.ACTIVE,
                        validate=(
                            validate.Range(min=constants.StatusEnum.min(),
                                           max=constants.StatusEnum.max())))
    config = fields.Raw()
    config_schema_version = fields.Integer(dump_only=True)
    element_js = fields.Str()
    element_css = fields.Str()
    date_created = fields.DateTime(dump_only=True)
    date_modified = fields.DateTime(dump_only=True)
    date_deleted = fields.DateTime(dump_only=True)


class GalleryElementSchema(PageElementSchema):
    attachements = fields.Nested(fields.Raw(), many=True)


class NodeTreeSchema(Schema):
    class Meta(object):
        strict = True
        ordered = True

    node = ResourceCreateSchema
    children = fields.Nested(ResourceCreateSchema, many=True)


class UserResourcePermissionSchema(Schema):
    class Meta(object):
        strict = True
        ordered = True

    user_name = fields.Str(required=True)

    perm_name = fields.Str(required=True)

    @validates('user_name')
    def validate_user_name(self, value):
        request = self.context['request']
        user = UserService.by_prefixed_user_name(value,
                                                 db_session=request.dbsession)
        if not user:
            raise validate.ValidationError(_('User not found'))

    @validates('perm_name')
    def validate_perm_name(self, value):
        perms = self.context['resource'].__possible_permissions__
        if value not in perms:
            raise validate.ValidationError(
                _('Incorrect permission name for resource'))


class GroupResourcePermissionSchema(Schema):
    class Meta(object):
        strict = True
        ordered = True

    group_id = fields.Int(required=True)

    perm_name = fields.Str(required=True)

    @validates('group_id')
    def validate_group_id(self, value):
        request = self.context['request']
        group = GroupService.get(value, db_session=request.dbsession)
        if not group:
            raise validate.ValidationError(_('Group not found'))

    @validates('perm_name')
    def validate_perm_name(self, value):
        perms = self.context['resource'].__possible_permissions__
        if value not in perms:
            raise validate.ValidationError(
                _('Incorrect permission name for resource'))


class UserPermissionSchema(Schema):
    class Meta(object):
        strict = True
        ordered = True

    perm_name = fields.Str(required=True)

    @validates('perm_name')
    def validate_perm_name(self, value):
        perms = self.context['resource'].__possible_permissions__
        if value not in perms:
            raise validate.ValidationError(
                _('Incorrect permission name for resource'))


class UploadSchema(Schema):
    class Meta(object):
        strict = True
        ordered = True

    uuid = fields.Str(dump_only=True)
    node_uuid = fields.Str(dump_only=True)
    original_filename = fields.Str(validate=(validate.Length(min=1, max=512)))
    filename = fields.Str(dump_only=True)
    slug = fields.Str(dump_only=True)
    extension = fields.Str(dump_only=True)
    name = fields.Str(validate=(validate.Length(min=1, max=512)))
    type = fields.Str(required=True, validate=(validate.Length(min=1, max=64)))
    description = fields.Str(validate=(validate.Length(min=1, max=2048)))
    status = fields.Int(default=constants.StatusEnum.ACTIVE,
                        validate=(validate.Range(min=0, max=1)))
    position = fields.Int(validate=(validate.Range(min=1)))
    config = fields.Raw()
    info = fields.Raw()


class UploadImageSchema(UploadSchema):
    class Meta(object):
        strict = True
        ordered = True

    base64_miniature = fields.Str(dump_only=True)
    miniature_filename = fields.Str(dump_only=True)
    upload_path = fields.Str(dump_only=True)


class ApplicationNodeConfigSchema(Schema):
    class Meta(object):
        strict = True
        ordered = True

    template_package = fields.String(default='', missing='')
    http_title = fields.String(default='', missing='')
    brand_html = fields.String(default='', missing='')
    index_node_uuid = fields.String(default='', missing='')

    @validates('index_node_uuid')
    def validate_index_node_uuid(self, value):
        if not value:
            return
        request = self.context['request']
        modified_obj = self.context.get('modified_obj')
        resource = ResourceService.by_uuid(
            value, tenant_pkey=request.context.application.resource_id,
            db_session=request.dbsession)
        if not resource:
            msg = _('Resource does not exist in the database')
            raise validate.ValidationError(msg)
