# -*- coding: utf-8 -*-
from pyramid.renderers import render
from ziggurat_cms.elements.blog.service import ElementBlogService
from ziggurat_cms.models.node_element import NodeElement
from ziggurat_cms.lib import safe_integer

class ZigguratCMSBlog(NodeElement):
    __mapper_args__ = {'polymorphic_identity': 'zigguratcms-blog'}

    def render(self, request, resource):
        # TODO: this is butt ugly - need to rewrite this to avoid circular
        # dependency, need a global storing service references?
        page = safe_integer(request.GET.get('page', 1))
        # url_maker gets passed to SqlalchemyOrmPage
        url_maker = lambda p: request.current_route_path(_query={"page": p})
        paginator = ElementBlogService.get_paginator(
            self, page=page, items_per_page=5,
            url_maker=url_maker)

        tmpl_vars = {
            'resource': resource,
            'element': self,
            'blog_entries_paginator': paginator,
            'element_dict': {e.uuid: e for e in resource.elements}
        }
        rendered = render(
            'ziggurat_cms:elements/blog/front_blog.jinja2',
            tmpl_vars, request=request)
        return rendered
