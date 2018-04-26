# -*- coding: utf-8 -*-

from ziggurat_cms.services.element_upload import ElementUploadImageBaseService
from ziggurat_cms.services.elements import BaseElementService


class ZigguratCMSQuillEditorService(BaseElementService):
    @classmethod
    def set_defaults(cls, instance):
        instance.config = {
            'delta': {},
            'compiled_html': ''
        }


class ElementUploadImageService(ElementUploadImageBaseService):
    pass
