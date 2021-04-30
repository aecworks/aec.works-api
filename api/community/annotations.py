from django.db import models as m

from . import choices
from .models import Comment, Company, CompanyRevision


def annotate_company_claps(qs, profile_id=-1):
    """
    Annotates Companies with `user_did_clap` indicating if provided
    profile has clapped
    """

    return qs.annotate(
        user_did_clap=m.Exists(
            Company.clappers.through.objects.filter(
                company_id=m.OuterRef("pk"), profile_id=profile_id
            )
        )
    )


def annotate_comment_claps(qs, profile_id=-1):
    return qs.annotate(
        user_did_clap=m.Exists(
            Comment.clappers.through.objects.filter(
                comment_id=m.OuterRef("pk"), profile_id=profile_id
            )
        )
    )


def annotate_company_count(qs):
    # TODO verify this is correct
    return qs.annotate(
        company_count=m.Count(
            "revisions",
            distinct=True,
            filter=m.Q(revisions__company__current_revision=m.F("id")),
        ),
    )
