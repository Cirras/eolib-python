from xml.etree.ElementTree import Element
from html import unescape


def get_instructions(element):
    return [
        child
        for child in element
        if isinstance(child, Element)
        and child.tag in ["field", "array", "length", "dummy", "switch", "chunked", "break"]
    ]


def get_comment(element):
    comment_element = next(
        (child for child in element if isinstance(child, Element) and child.tag == "comment"), None
    )

    if comment_element is not None:
        return get_text(comment_element)

    return None


def get_text(element):
    result = (element.text if element.text else "").strip()
    result = result.strip()

    for child in element:
        text = (child.tail if child.tail else "").strip()
        if text:
            if result:
                raise RuntimeError(f'Unexpected text content "{text}"')
            result = text

    return unescape(result) if result else None


def get_string_attribute(element, name, default_value=None):
    attribute_text = element.get(name)
    if attribute_text is None:
        return default_value
    return attribute_text


def get_int_attribute(element, name, default_value=0):
    attribute_text = element.get(name)
    if attribute_text is None:
        return default_value
    try:
        return int(attribute_text)
    except ValueError:
        raise ValueError(f'{name} attribute has an invalid integer value: {attribute_text.strip()}')


def get_boolean_attribute(element, name, default_value=False):
    attribute_text = element.get(name)
    if attribute_text is None:
        return default_value
    return attribute_text.lower() == "true"


def get_required_string_attribute(element, name):
    attribute_value = element.get(name)
    if attribute_value is None:
        raise ValueError(f'Required attribute "{name}" is missing.')
    return attribute_value


def get_required_int_attribute(element, name):
    attribute_value = element.get(name)
    if attribute_value is None:
        raise ValueError(f'Required attribute "{name}" is missing.')
    try:
        return int(attribute_value)
    except ValueError:
        raise ValueError(
            f'{name} attribute has an invalid integer value: {attribute_value.strip()}'
        )


def get_required_boolean_attribute(element, name):
    attribute_value = element.get(name)
    if attribute_value is None:
        raise ValueError(f'Required attribute "{name}" is missing.')
    return attribute_value.lower() == "true"
