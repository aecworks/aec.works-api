import graphene

from api import community
from .types import PostType


class CreatePost(graphene.Mutation):
    class Arguments:
        # Replaces Serializers
        title = graphene.String(required=True)
        body = graphene.String(required=True)
        hashtag_names = graphene.List(graphene.String)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        profile = info.context.user.profile
        post = community.services.create_post(profile=profile, **kwargs)
        return cls(post=post)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
