from django.db import models
from api.common.lookups import Floor
from mptt.querysets import TreeQuerySet
from django.apps import apps


class CommentQueryset(TreeQuerySet):
    def with_counts(self):
        """ Adds `clas_count` and `comment_count` to queryset """
        # Annotate across 2+ tables generate incorrect results unless disctinct is added
        # https://code.djangoproject.com/ticket/25861#comment:3
        return self.annotate(
            clap_count=models.Count("clappers", distinct=True),
            comment_count=models.Count("replies", distinct=True),
        )


class CompanyQueryset(models.QuerySet):
    def with_counts(self):
        """ Adds `clas_count` and `comment_count` to queryset """
        qs = self.annotate(clap_count=models.Count("clappers", distinct=True))
        return annotate_with_comment_count(qs)


class PostQueryset(models.QuerySet):
    def with_counts(self):
        """ Adds `clas_count` and `comment_count` to queryset """
        qs = self.annotate(clap_count=models.Count("clappers", distinct=True))
        return annotate_with_comment_count(qs)


def annotate_with_comment_count(queryset):
    """
    Helper Method to annotate a queryset with `comment_count
    Queryset object must have a 'thread_id' attribute

    This Queryset recursively count the total number of comments in the threadself using
    duplicating mptt strategy for get_ancestor_count().

    With this we can get for example, all posts at once including the total nested
    comment count in its thread in a single query. Uf!

    Usage:
        >>> Post.objects.with_count().first().comment_count
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
        comment_count=models.F("_ancestor_count")
        + models.Count("thread__comments", distinct=True)
    )
