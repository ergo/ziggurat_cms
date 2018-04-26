# -*- coding: utf-8 -*-

import logging

from ziggurat_cms.models.element_upload import ElementUploadFile
from ziggurat_cms.services.element_upload import ElementUploadBaseService

log = logging.getLogger(__name__)


class ElementUploadFileService(ElementUploadBaseService):
    @classmethod
    def bump_downloads(cls, instance):
        instance.downloads = ElementUploadFile.downloads + 1
