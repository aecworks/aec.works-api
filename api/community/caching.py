from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from api.common.utils import delete_cache_key

from . import models, selectors


class CachePrefix:
    HASHTAG_LIST = "hashtag_list_get"
    COMPANY_LIST = "company_list_get"


def hashtag_last_modified(request) -> str:
    lastmod = selectors.get_hashtags_simple().order_by("updated_at").last()
    return lastmod.updated_at


def company_last_modified(request) -> str:
    lastmod = selectors.get_companies().order_by("updated_at").last()
    return lastmod.updated_at


@receiver(post_save, sender=models.Hashtag)
@receiver(post_delete, sender=models.Hashtag)
def delete_hash_cache(sender, instance, **kwargs):
    delete_cache_key(CachePrefix.HASHTAG_LIST)


@receiver(post_save, sender=models.Article)
@receiver(post_delete, sender=models.Article)
@receiver(post_save, sender=models.Company)
@receiver(post_delete, sender=models.Company)
@receiver(post_save, sender=models.Company.clappers.through)
@receiver(post_delete, sender=models.Company.clappers.through)
@receiver(post_save, sender=models.Thread)
@receiver(post_delete, sender=models.Thread)
@receiver(post_save, sender=models.Hashtag)
@receiver(post_delete, sender=models.Hashtag)
def delete_list_cache(sender, instance, **kwargs):
    delete_cache_key(CachePrefix.COMPANY_LIST)
