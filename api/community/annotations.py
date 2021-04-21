from django.db import models as m

from .models import Comment, Company


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
