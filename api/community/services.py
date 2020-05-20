from .models import Comment


def post_clap(*, post, user):
    if not user.is_anonymous:
        post.clappers.add(user.profile)
    return post.clappers.count()


def create_thread_comment(*, profile, thread, text):
    return Comment.objects.create(profile=profile, thread=thread, text=text)
