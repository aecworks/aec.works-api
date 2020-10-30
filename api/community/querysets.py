from django.db import models
from api.common.lookups import Floor
from mptt.querysets import TreeQuerySet
from django.apps import apps


class HashtagQueryset(models.QuerySet):
    def with_counts(self):
        """ Adds `counts` queryset """
        qs = self.annotate(
            company_count=models.Count("companies", distinct=True),
            post_count=models.Count("posts", distinct=True),
        )
        return qs
