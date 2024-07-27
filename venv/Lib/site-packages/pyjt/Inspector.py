""" Inspect UI components """

import logging
from lxml import etree

log = logging.getLogger(__name__)

_fields = ['name', 'class', 'text', 'title']


class Inspector:
    """ Helper class for inspecting the component tree of a specific component.
    """
    @staticmethod
    def inspect(component):
        """ Inspects the component tree of a component.

            Args:
                component (Fixture):
                    The component to inspect.

            Returns:
                dict:
                    A dictionary with information of all sub-components
                    for this component.
        """
        result = {}
        for field in _fields:
            _set_field(result, component, field)

        result['childs'] = []
        if not hasattr(component, 'getComponents'):
            return result
        for child in component.components():
            result['childs'].append(Inspector.inspect(child))
        return result

    @staticmethod
    def etree(component):
        return Inspector.etreemap(component)[0]

    @staticmethod
    def etreemap(component, mapping=None):
        if not mapping:
            mapping = {}
        _id = id(component)
        mapping[_id] = component
        element = etree.Element(str(component.getClass().getSimpleName()))
        for field in _fields:
            value = _get_attribute(component, field)
            if value is not None:
                element.set(field, value)
        element.set("_id", str(_id))

        for subelement in component.components():
            element.append(Inspector.etreemap(subelement, mapping)[0])
        return (element, mapping)


@staticmethod
def _set_field(result, component, field):
    value = _get_attribute(component, field)
    if value is not None:
        result[field] = value


def _get_attribute(component, attribute):
    func = f'get{attribute.title()}'
    if not hasattr(component, func):
        return None
    value = getattr(component, func)()
    if value is not None:
        return str(value)
    return ""
