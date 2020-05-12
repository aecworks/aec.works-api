def post_clap(*, post, user):
    if not user.is_anonymous:
        post.clappers.add(user.profile)
    return post.clappers.count()
