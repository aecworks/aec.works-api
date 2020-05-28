from rest_framework import serializers


def inline_serializer(*, fields, data=None, **kwargs):
    """ 'Hello Text!' -> 'hello-text' """
    serializer_class = type("InlineSerializer", (serializers.Serializer,), fields)
    if data is not None:
        return serializer_class(data=data, **kwargs)
    return serializer_class(**kwargs)
