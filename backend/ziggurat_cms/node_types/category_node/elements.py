from pyramid.renderers import render


class CategoryNodeListElement(object):
    def render(self, request, resource):
        tmpl_vars = {
            'resource': resource,
            'element': self,
            'children': resource.children,
            'element_dict': {}
        }
        rendered = render(
            'ziggurat_cms:node_types/category_node/templates/node_list.jinja2',
            tmpl_vars, request=request)
        return rendered
