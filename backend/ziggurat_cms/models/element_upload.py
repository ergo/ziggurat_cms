# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import uuid

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from ziggurat_cms.constants import StatusEnum
from ziggurat_cms.models.meta import Base
from ziggurat_cms.models.mixins import ModifiedTimesMixin
from ziggurat_foundations.models.base import BaseModel


class ElementUpload(Base, ModifiedTimesMixin, BaseModel):
    __tablename__ = 'elements_uploads'
    __mapper_args__ = {'polymorphic_on': 'type'}

    pkey = sa.Column(sa.Integer(), primary_key=True)
    element_pkey = sa.Column(sa.Integer(),
                             sa.ForeignKey('node_elements.pkey',
                                           onupdate='CASCADE',
                                           ondelete='CASCADE', ))
    resource_id = sa.Column(sa.Integer(),
                            sa.ForeignKey('resources.resource_id',
                                          onupdate='CASCADE',
                                          ondelete='CASCADE', ))
    sub_key = sa.Column(sa.Integer())
    uuid = sa.Column('uuid', postgresql.UUID,
                     default=lambda x: str(uuid.uuid4()))
    status = sa.Column(sa.SmallInteger(), default=StatusEnum.ACTIVE.value)
    config = sa.Column(postgresql.JSONB(), default=dict)
    info = sa.Column(postgresql.JSONB(), default=dict)
    original_filename = sa.Column('original_filename', sa.Unicode(512),
                                  nullable=False)
    filename = sa.Column('filename', sa.Unicode(512), nullable=False)
    slug = sa.Column('slug', sa.Unicode(512))
    name = sa.Column('name', sa.Unicode(128))
    extension = sa.Column('extension', sa.Unicode(8))
    size = sa.Column('size', sa.Integer, default=0)
    type = sa.Column('type', sa.Unicode(64), nullable=False)
    from_element = sa.Column('from_element', sa.Unicode(64))
    description = sa.Column('description', sa.UnicodeText)
    position = sa.Column('position', sa.Integer(), default=1,
                         nullable=False, index=True)
    upload_path = sa.Column('upload_path',
                            sa.Unicode(2048), nullable=False, default='')
    info_schema_version = sa.Column(
        'info_schema_version', sa.Integer, default=1),
    config_schema_version = sa.Column(
        'config_schema_version', sa.Integer, default=1)

    element = sa.orm.relationship(
        'NodeElement',
        passive_deletes=True,
        passive_updates=True,
        uselist=False)

    resource = sa.orm.relationship(
        'Resource',
        passive_deletes=True,
        passive_updates=True,
        uselist=False)


class ElementUploadImage(ElementUpload):
    __tablename__ = 'zigguratcms_uploads_images'
    __mapper_args__ = {'polymorphic_identity': 'zigguratcms-upload-files-image'}
    pkey = sa.Column('pkey', sa.BigInteger(),
                     sa.ForeignKey('elements_uploads.pkey',
                                   onupdate='CASCADE',
                                   ondelete='CASCADE'), primary_key=True)
    base64_miniature = sa.Column('base64_miniature', sa.Unicode(4096),
                                 default=None)
    miniature_filename = sa.Column('miniature_filename', sa.Unicode(512))


class ElementUploadFile(ElementUpload):
    __tablename__ = 'zigguratcms_uploads_files'
    __mapper_args__ = {'polymorphic_identity': 'zigguratcms-upload-files-file'}
    pkey = sa.Column('pkey', sa.BigInteger(),
                     sa.ForeignKey('elements_uploads.pkey',
                                   onupdate='CASCADE',
                                   ondelete='CASCADE'), primary_key=True)
    downloads = sa.Column('downloads', sa.Integer, default=0, nullable=False)
