from django.db import models
from api.common.lookups import Floor
from mptt.querysets import TreeQuerySet
from django.apps import apps


class CommentQueryset(TreeQuerySet):
    def with_counts(self):
        """
        Adds `clap_count` and `reply_count` to queryset
        `reply_count` is not recursive - only direct child comments
        """
        return self.annotate(
            clap_count=models.Count("clappers", distinct=True),
            reply_count=models.Count("replies", distinct=True),
        )
        # distinct= needed bcse annotate across 2+ tables generates incorrect results
        # https://code.djangoproject.com/ticket/25861#comment:3


class CompanyQueryset(models.QuerySet):
    def with_counts(self):
        """ Adds `clap_count` and `thread_size` to queryset """
        qs = self.annotate(clap_count=models.Count("clappers", distinct=True))
        return annotate_with_thread_size(qs)


class HashtagQueryset(models.QuerySet):
    def with_counts(self):
        """ Adds `counts` queryset """
        qs = self.annotate(
            company_count=models.Count("companies", distinct=True),
            post_count=models.Count("posts", distinct=True),
        )
        return qs


class PostQueryset(models.QuerySet):
    def with_counts(self):
        """ Adds `clap_count` and `thread_size` to queryset """
        qs = self.annotate(clap_count=models.Count("clappers", distinct=True))
        return annotate_with_thread_size(qs)


def annotate_with_thread_size(queryset):
    """
    Helper Method to annotate a queryset with `thread_size`self.
    Queryset object must have a 'thread_id' attribute

    `thread_size` is an integer representing the recursive count the total number
    of comments in the threadself.
    It duplicates mptt strategy for get_ancestor_count().

    Usage:
        >>> Post.objects.with_count().first().thread_size
        6

        Comment
            Thread
            + Comment           1
            + Comment        2
            + Comment        3
                + Comment      4
                + Comment    5
            + Comment           6
    """
    # See
    # https://stackoverflow.com/questions/20139372/django-queryset-attach-or-annotate-related-object-field/47725075
    # this query reproduces the get_descendant_count() logic for each top level comment
    # https://django-mptt.readthedocs.io/en/latest/models.html#get-descendant-count

    Thread = apps.get_model("community.Thread")
    threads = Thread.objects.filter(id=models.OuterRef("thread_id")).annotate(
        _ancestor_count=models.Sum(
            Floor((models.F("comments__rght") - models.F("comments__lft") - 1) / 2)
        )
    )
    # Comment count subquery includes "descendent count", but the top level comment
    # itself is not included, so we add that on top.
    return queryset.annotate(
        _ancestor_count=models.Subquery(
            threads.values("_ancestor_count")[:1], output_field=models.IntegerField(),
        )
    ).annotate(
        thread_size=models.F("_ancestor_count")
        + models.Count("thread__comments", distinct=True)
    )
