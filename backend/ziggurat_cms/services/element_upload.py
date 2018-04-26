# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import base64
import logging
import math
import os
import shutil
from collections import namedtuple
from io import BytesIO

from PIL import Image
from ziggurat_cms.models.element_upload import ElementUpload
from ziggurat_cms.lib import generate_slug_text
from ziggurat_foundations.models.services import BaseService

log = logging.getLogger(__name__)

FileNameTuple = namedtuple('FileNameTuple',
                           ['filename', 'orginal_filename', 'extension'])


class ElementUploadBaseService(BaseService):
    @classmethod
    def gen_directory(cls, root_dir, path_dir, pkey=None):
        abs_upload_dir = os.path.abspath(os.path.join(root_dir, path_dir))
        if not os.path.exists(abs_upload_dir):
            os.mkdir(abs_upload_dir, mode=0o774)

        if pkey is None:
            return abs_upload_dir

        milions = math.floor(pkey / 1000000)
        abs_mil_path = os.path.abspath(
            os.path.join(root_dir, path_dir, str(milions)))
        if not os.path.exists(abs_mil_path):
            os.mkdir(abs_mil_path, mode=0o774)

        thousands = math.floor((pkey - milions * 1000000) / 5000)
        final_path = os.path.join(path_dir, str(milions), str(thousands))
        abs_final_path = os.path.abspath(
            os.path.join(root_dir, final_path))
        if not os.path.exists(abs_final_path):
            os.mkdir(abs_final_path, mode=0o774)
        return abs_final_path

    @classmethod
    def gen_filename(cls, pkey, prefix, filename):
        orginal_filename = os.path.basename(filename)
        extension = None
        split_ext = os.path.splitext(orginal_filename)
        if len(split_ext) > 1:
            extension = split_ext[1]
        name = generate_slug_text(orginal_filename, allow_dots=True)
        filename = '{}_{}_{}'.format(pkey, prefix, name)
        return FileNameTuple(filename, orginal_filename, extension[1:])

    @classmethod
    def save_file(cls, file_obj, upload_dir, filename):
        final_path = os.path.abspath(os.path.join(upload_dir, filename))
        try:
            log.info('copying to %s' % upload_dir)
            shutil.copyfileobj(file_obj, open(final_path, 'w+b'))
        except Exception as exc:
            log.error(str(exc), extra={
                'file_name': filename,
                'upload_dir': upload_dir,
                'exception_message': str(exc),
                'callable': 'ElementUploadService.save_file'
            })
            raise

    @classmethod
    def delete_file(cls, root_dir, upload_dir, filename):
        final_path = os.path.abspath(
            os.path.join(root_dir, upload_dir, filename))
        try:
            os.remove(final_path)
        except Exception as exc:
            log.error(
                str(exc), extra={
                    'file_name': filename,
                    'final_path': final_path,
                    'callable': 'ElementUploadService.delete_file'
                })

    @classmethod
    def by_uuid(cls, uuid, db_session):
        query = db_session.query(ElementUpload)
        query = query.filter(ElementUpload.uuid == uuid)
        return query.first()


class ElementUploadImageBaseService(ElementUploadBaseService):
    @classmethod
    def get_image_obj(cls, file_obj):
        return Image.open(file_obj)

    @classmethod
    def save_resized_image(cls, image_obj, filename, upload_dir, max_size):
        final_path = os.path.abspath(os.path.join(upload_dir, filename))
        if image_obj.size[0] > max_size[0] or image_obj.size[1] > max_size[1]:
            copied = image_obj.copy()
            copied.thumbnail(max_size)
            copied.save(final_path)
        else:
            image_obj.save(final_path)

    @classmethod
    def base64_thumbnail(cls, image_obj, size):
        image_obj.thumbnail(size)
        jpg_fp = BytesIO()
        image_obj.save(jpg_fp, format='jpeg')
        encoded = base64.b64encode(jpg_fp.getvalue())
        return encoded.decode()
