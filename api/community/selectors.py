from .models import Company, Comment, Post, Hashtag, Thread


def get_comments():
    return Comment.objects.select_related("profile__user").with_counts().all()


def get_thread(*, id):
    return Thread.objects.get(id=id)


def get_thread_comments(*, thread_id):
    return get_comments().filter(level=0, thread_id=thread_id)


def get_comment_children(*, parent_id):
    return get_comments().filter(parent_id=parent_id)


def get_companies():
    return (
        Company.objects.select_related(
            "profile", "thread", "approved_by", "replaced_by", "revision_of"
        )
        .prefetch_related("hashtags")
        .with_counts()
        .all()
    )


def get_hashtags():
    return Hashtag.objects.all()


def get_posts():
    return (
        Post.objects.select_related("profile__user")
        .prefetch_related("hashtags", "companies", "thread__comments")
        .with_counts()
        .all()
    )
