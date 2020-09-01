import string
from rest_framework import serializers
from rest_framework.utils import model_meta


def inline_serializer(*, fields, data=None, **kwargs):
    """ 'Hello Text!' -> 'hello-text' """
    serializer_class = type("InlineSerializer", (serializers.Serializer,), fields)
    if data is not None:
        return serializer_class(data=data, **kwargs)
    return serializer_class(**kwargs)


def update_instance(instance, validated_data):
    # from drf ModelSerializer.update()
    info = model_meta.get_field_info(instance)

    m2m_fields = []
    for attr, value in validated_data.items():
        if attr in info.relations and info.relations[attr].to_many:
            m2m_fields.append((attr, value))
        else:
            setattr(instance, attr, value)

    instance.save()
    # Note that many-to-many fields are set after updating instance.
    # Setting m2m fields triggers signals which could potentially change
    # updated instance and we do not want it to collide with .update()
    for attr, value in m2m_fields:
        field = getattr(instance, attr)
        field.set(value)

    return instance


def to_hashtag(text: str):
    """ Only leters, no symbols but allows case """
    return "".join([c for c in text if c in string.ascii_letters])
