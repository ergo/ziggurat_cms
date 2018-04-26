"""initial migration

Revision ID: afez8c2875e5
Revises:
Create Date: 2016-11-26 11:26:28.732074

"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as postgresql
from alembic import op

# revision identifiers, used by Alembic.
revision = 'afez8c2875e5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('resources',
                  sa.Column('uuid', postgresql.UUID, nullable=False,
                            unique=True))
    op.add_column('resources',
                  sa.Column('parent_uuid', postgresql.UUID))
    op.add_column('resources',
                  sa.Column('current_slug', sa.Unicode(512), index=True,
                            nullable=True))
    op.add_column('resources',
                  sa.Column('date_created', sa.DateTime, index=True,
                            nullable=True))
    op.add_column('resources',
                  sa.Column('date_modified', sa.DateTime, index=True,
                            nullable=True))
    op.add_column('resources',
                  sa.Column('date_deleted', sa.DateTime, index=True,
                            nullable=True))
    op.add_column('resources',
                  sa.Column('tenant_pkey', sa.Integer, index=True))
    op.add_column('resources',
                  sa.Column('status', sa.SmallInteger, nullable=False))
    op.add_column('resources',sa.Column('config', postgresql.JSONB(), nullable=False))
    op.add_column('resources',sa.Column('config_schema_version', sa.Integer))

    op.add_column('users', sa.Column('uuid', postgresql.UUID, nullable=False))
    op.add_column('users', sa.Column(
        'tenant_pkey', sa.Integer,
        sa.ForeignKey('resources.resource_id',
                      onupdate='CASCADE',
                      ondelete='CASCADE')))
    op.add_column('users',
                  sa.Column('public_user_name', sa.String(128), nullable=False))
    op.add_column('users',
                  sa.Column('public_email', sa.String(128), nullable=False))
    op.add_column('groups', sa.Column('uuid', postgresql.UUID, nullable=False))
    op.add_column('groups', sa.Column(
        'tenant_pkey', sa.Integer,
        sa.ForeignKey('resources.resource_id',
                      onupdate='CASCADE',
                      ondelete='CASCADE')))

    op.create_table(
        'organizations',
        sa.Column('resource_id', sa.Integer(),
                  sa.ForeignKey('resources.resource_id',
                                onupdate='CASCADE',
                                ondelete='CASCADE'),
                  primary_key=True),
        sa.Column('description', sa.UnicodeText)
    )

    op.create_table(
        'applications',
        sa.Column('resource_id', sa.Integer(),
                  sa.ForeignKey('resources.resource_id',
                                onupdate='CASCADE',
                                ondelete='CASCADE'),
                  primary_key=True),
        sa.Column('description', sa.UnicodeText),
        sa.Column('node_info', postgresql.JSONB, nullable=False),
        sa.Column('node_js', sa.UnicodeText),
        sa.Column('node_css', sa.UnicodeText),
        sa.Column('node_info_schema_version', sa.Integer)
    )

    op.create_table(
        'applications_domains',
        sa.Column('resource_id', sa.Integer(),
                  sa.ForeignKey('resources.resource_id',
                                onupdate='CASCADE',
                                ondelete='CASCADE'),
                  primary_key=True),
        sa.Column('domain', sa.Unicode(256), primary_key=True,
                  unique=True)
    )

    op.create_table(
        'zigguratcms_page_nodes',
        sa.Column('resource_id', sa.Integer(),
                  sa.ForeignKey('resources.resource_id',
                                onupdate='CASCADE',
                                ondelete='CASCADE'),
                  primary_key=True),
        sa.Column('resource_uuid', postgresql.UUID,
                  sa.ForeignKey('resources.uuid',
                                onupdate='CASCADE',
                                ondelete='CASCADE', ),
                  index=True),
        sa.Column('description', sa.UnicodeText),
        sa.Column('node_js', sa.UnicodeText),
        sa.Column('node_css', sa.UnicodeText),
        sa.Column('version', sa.Integer)
    )

    op.create_table(
        'zigguratcms_blog_nodes',
        sa.Column('resource_id', sa.Integer(),
                  sa.ForeignKey('resources.resource_id',
                                onupdate='CASCADE',
                                ondelete='CASCADE'),
                  primary_key=True),
        sa.Column('resource_uuid', postgresql.UUID,
                  sa.ForeignKey('resources.uuid',
                                onupdate='CASCADE',
                                ondelete='CASCADE', ),
                  index=True),
        sa.Column('description', sa.UnicodeText),
        sa.Column('node_js', sa.UnicodeText),
        sa.Column('node_css', sa.UnicodeText),
        sa.Column('version', sa.Integer)
    )

    op.create_table(
        'node_elements',
        sa.Column('pkey', sa.Integer(), primary_key=True),
        sa.Column('tenant_pkey', sa.Integer, index=True),
        sa.Column('resource_id', sa.Integer(),
                  sa.ForeignKey('resources.resource_id',
                                onupdate='CASCADE',
                                ondelete='CASCADE', ),
                  index=True),
        sa.Column('uuid', postgresql.UUID, nullable=False, index=True,
                  unique=True),
        sa.Column('parent_element_pkey', sa.Integer(),
                  sa.ForeignKey('node_elements.pkey',
                                onupdate='CASCADE',
                                ondelete='CASCADE', ),
                  index=True),
        sa.Column('resource_uuid', postgresql.UUID,
                  sa.ForeignKey('resources.uuid',
                                onupdate='CASCADE',
                                ondelete='CASCADE', ),
                  index=True),
        sa.Column('list_for_resource', sa.Boolean, nullable=False, index=True),
        sa.Column('type', sa.Unicode(64), nullable=False, index=True),
        sa.Column('status', sa.SmallInteger(), nullable=False, index=True),
        sa.Column('config', postgresql.JSONB(), nullable=False),
        sa.Column('element_js', sa.UnicodeText),
        sa.Column('element_css', sa.UnicodeText),
        sa.Column('version', sa.Integer),
        sa.Column('config_schema_version', sa.Integer),
        sa.Column('current_slug', sa.Unicode(512), index=True,
                  nullable=True)
    )
    op.add_column('node_elements',
                  sa.Column('date_created', sa.DateTime, index=True,
                            nullable=False))
    op.add_column('node_elements',
                  sa.Column('date_modified', sa.DateTime, index=True,
                            nullable=False))
    op.add_column('node_elements',
                  sa.Column('date_deleted', sa.DateTime, index=True,
                            nullable=True))

    op.create_table(
        'elements_uploads',
        sa.Column('pkey', sa.BigInteger(), primary_key=True),
        sa.Column('resource_id', sa.Integer(),
                  sa.ForeignKey('resources.resource_id',
                                onupdate='CASCADE',
                                ondelete='SET NULL', ),
                  index=True),
        sa.Column('element_pkey', sa.Integer(),
                  sa.ForeignKey('node_elements.pkey',
                                onupdate='CASCADE',
                                ondelete='SET NULL', ),
                  index=True),
        sa.Column('sub_key', sa.Integer()),
        sa.Column('resource_uuid', postgresql.UUID,
                  sa.ForeignKey('resources.uuid',
                                onupdate='CASCADE',
                                ondelete='CASCADE', ),
                  index=True),
        sa.Column('parent_element_uuid', postgresql.UUID,
                  sa.ForeignKey('node_elements.uuid',
                                onupdate='CASCADE',
                                ondelete='CASCADE', ),
                  index=True),
        sa.Column('sub_uuid', postgresql.UUID,
                  sa.ForeignKey('node_elements.uuid',
                                onupdate='CASCADE',
                                ondelete='CASCADE', ),
                  index=True),
        sa.Column('uuid', postgresql.UUID, nullable=False, unique=True),
        sa.Column('original_filename', sa.Unicode(512), nullable=False),
        sa.Column('filename', sa.Unicode(512), nullable=False),
        sa.Column('extension', sa.Unicode(8)),
        sa.Column('size', sa.Integer),
        sa.Column('type', sa.Unicode(64), nullable=False),
        sa.Column('from_element', sa.Unicode(64), nullable=False),
        sa.Column('slug', sa.Unicode(512), nullable=False),
        sa.Column('name', sa.Unicode(128), nullable=False),
        sa.Column('description', sa.UnicodeText),
        sa.Column('config', postgresql.JSONB(), nullable=False),
        sa.Column('config_schema_version', sa.Integer),
        sa.Column('info', postgresql.JSONB(), nullable=False),
        sa.Column('status', sa.SmallInteger(), nullable=False, index=True),
        sa.Column('position', sa.Integer(), nullable=False, index=True),
        sa.Column('upload_path', sa.Unicode(4096), nullable=False, default=''),
        sa.Column('date_created', sa.DateTime, index=True,
                  nullable=False),
        sa.Column('date_modified', sa.DateTime, index=True,
                  nullable=False),
        sa.Column('date_deleted', sa.DateTime, index=True,
                  nullable=True),
        sa.Column('info_schema_version', sa.Integer)
    )

    op.create_table(
        'zigguratcms_uploads_images',
        sa.Column('pkey', sa.BigInteger(),
                  sa.ForeignKey('elements_uploads.pkey',
                                onupdate='CASCADE',
                                ondelete='CASCADE'), primary_key=True),
        sa.Column('base64_miniature', sa.Unicode(8192), default=None),
        sa.Column('miniature_filename', sa.Unicode(512))
    )

    op.create_table(
        'zigguratcms_uploads_files',
        sa.Column('pkey', sa.BigInteger(),
                  sa.ForeignKey('elements_uploads.pkey',
                                onupdate='CASCADE',
                                ondelete='CASCADE'), primary_key=True),
        sa.Column('downloads', sa.Integer, default=0, nullable=False)
    )

    op.create_table(
        'zigguratcms_blog_entries',
        sa.Column('pkey', sa.BigInteger(),
                  sa.ForeignKey('node_elements.pkey',
                                onupdate='CASCADE',
                                ondelete='CASCADE'), primary_key=True),
        sa.Column('name', sa.Unicode(256), nullable=False),
        sa.Column('tags', postgresql.JSONB(), nullable=False)
    )

    op.create_table(
        'slugs',
        sa.Column('pkey', sa.BigInteger(), primary_key=True),
        sa.Column('resource_id', sa.Integer(),
                  sa.ForeignKey('resources.resource_id',
                                onupdate='CASCADE',
                                ondelete='CASCADE'), index=True),
        sa.Column('element_pkey', sa.Integer(),
                  sa.ForeignKey('node_elements.pkey',
                                onupdate='CASCADE',
                                ondelete='CASCADE'), index=True),
        sa.Column('uuid', postgresql.UUID, nullable=False, unique=True),
        sa.Column('text', sa.Unicode(512), index=True),
        sa.Column('counter', sa.Integer, nullable=False),
        sa.Column('tenant_pkey', sa.Integer, index=True, nullable=False),
    )
    op.create_index('uq_slugs_text_tenant_pkey_counter',
                    'slugs', ['text', 'tenant_pkey', 'counter'], unique=True)

    op.create_table(
        'auth_tokens',
        sa.Column('pkey', sa.Integer, primary_key=True),
        sa.Column('uuid', postgresql.UUID),
        sa.Column('token', postgresql.UUID),
        sa.Column('name', sa.Unicode(128)),
        sa.Column('description', sa.Unicode(512)),
        sa.Column('created', sa.DateTime),
        sa.Column('expires', sa.DateTime),
        sa.Column('owner_id', sa.Integer,
                  sa.ForeignKey('users.id', onupdate='cascade',
                                ondelete='cascade'))
    )


def downgrade():
    pass
