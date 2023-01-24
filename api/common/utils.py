import logging
import operator
import string

import requests
from django.core.cache import cache
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify as _slugify
from opengraph.opengraph import OpenGraph
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.utils import model_meta

logger = logging.getLogger(__name__)


def inline_serializer(*, fields, data=None, **kwargs):
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
        if value.__class__.__name__ == "ManyRelatedManager":
            value = value.all()
        field.set(value)

    return instance


def to_hashtag(text: str) -> str:
    """Only leters, no symbols but allows case"""
    return "".join([c for c in text if c in string.ascii_letters + string.digits])


def slugify(text: str) -> str:
    # https://docs.djangoproject.com/en/3.2/ref/utils/#django.utils.text.slugify
    """
    >>> slugify(' Joel is a slug ')
    'joel-is-a-slug'
    """
    return _slugify(text)


def increment_slug(slug: str) -> str:
    chunks = slug.split("-")

    if len(chunks) == 1:
        return f"{slug}-2"

    *names, last = chunks

    if not last.isdigit():
        return f"{slug}-2"

    num = int(last) + 1
    return "-".join(names) + f"-{num}"


def get_og_data(url: str):

    resp = requests.get(url)
    if not resp.ok:
        logger.info(f"could not get opengraph data for url: {url}: {resp}")
        return {}

    og_data = None
    og_article = OpenGraph(html=resp.content, scrape=True)
    if og_article.is_valid():
        tags = [
            "site_name",
            "type",
            "title",
            "description",
            "image",
            "image:alt",
            "image:height",
            "image:width",
        ]
        og_data = {k: v for k, v in og_article.items() if k in tags}
    return og_data


def admin_linkify(field_name):
    """
    Converts a foreign key value into clickable links.

    If field_name is 'parent', link text will be str(obj.parent)
    Link will be admin url for the admin url for obj.parent.id:change
    """

    def _linkify(obj):
        linked_obj = operator.attrgetter(field_name)(obj)
        if linked_obj is None:
            return "-"
        app_label = linked_obj._meta.app_label
        model_name = linked_obj._meta.model_name
        view_name = f"admin:{app_label}_{model_name}_change"
        link_url = reverse(view_name, args=[linked_obj.pk])
        return format_html('<a href="{}">{}</a>', link_url, linked_obj)

    _linkify.short_description = field_name  # Sets column name
    return _linkify


def admin_related(related, attr):
    def _wrap(obj):
        return getattr(getattr(obj, related), attr)

    _wrap.short_description = f"{related}:{attr}"
    return _wrap


def delete_cache_key(key_prefix):
    keys = [k for k in cache.keys("*") if f".{key_prefix}." in k]
    logger.info(f"deteling cache keys: {len(keys)}")
    cache.delete_many(keys)


def validate_or_raise(SerializerCls, data):
    serializer = SerializerCls(data=data)
    if not serializer.is_valid():
        logger.error(f"cannot serializer: cls:{SerializerCls} data:{data}")
        raise APIException("server validation error logged")
    return serializer
