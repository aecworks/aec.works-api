from rest_framework import serializers


def to_slug(text):
    """ 'Hello Text!' -> 'hello-text' """
    return "".join(
        [c for c in text.replace(" ", "-").lower() if c.isalpha() or c == "-"]
    )


def inline_serializer(*, fields, data=None, **kwargs):
    """ 'Hello Text!' -> 'hello-text' """
    serializer_class = type("InlineSerializer", (serializers.Serializer,), fields)
    if data is not None:
        return serializer_class(data=data, **kwargs)
    return serializer_class(**kwargs)
