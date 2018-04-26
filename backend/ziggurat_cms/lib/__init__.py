# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
import re
from uuid import UUID

from pyramid.httpexceptions import HTTPBadRequest
from text_unidecode import unidecode

log = logging.getLogger(__name__)


def safe_integer(integer):
    try:
        return int(integer)
    except (ValueError, TypeError):
        log.error('Incorrect integer {}, '
                  'raising HTTPBadRequest'.format(integer))
        raise HTTPBadRequest()


def safe_uuid(uid):
    try:
        if isinstance(uid, UUID):
            return str(uid)
        return str(UUID(uid))
    except (ValueError, TypeError):
        log.error('Incorrect uuid {}, '
                  'raising HTTPBadRequest'.format(uid))
        raise HTTPBadRequest()


def session_provider(request):
    """ provides sqlalchemy session for ziggurat_foundations """
    return request.dbsession


def generate_slug_text(text, allow_dots=False, to_lower=True):
    pattern = '[^a-zA-Z0-9_]'
    if allow_dots:
        pattern = '[^a-zA-Z0-9_\.]'
    processed = re.sub(pattern, '-', unidecode(text).strip()) or ''
    if to_lower:
        processed = processed.lower()
    output = []
    for c in processed:
        if not output and c != '-' or output and output[-1] != '-' or c != '-':
            output.append(c)
    if output and output[-1] == '-':
        output = output[:-1]
    return ''.join(output)


def populate_obj_from_dict(instance,
                           dictionary, exclude_keys=None, include_keys=None):
    """
    updates instance properties *for column names that exist*
    for this model and are keys present in passed dictionary
    :param dictionary: (dictionary)
    :param exclude_keys: (optional) is a list of columns from model that
    should not be updated by this function
    :param include_keys: (optional) is a list of columns from model that
    should be updated by this function
    :return:
    """
    exclude_keys_list = exclude_keys or []
    include_keys_list = include_keys or []
    for k in dictionary._get_keys():
        if k not in exclude_keys_list and \
                (k in include_keys_list or not include_keys):
            setattr(instance, k, dictionary[k])
