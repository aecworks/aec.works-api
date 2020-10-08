import graphene
from graphene_django import DjangoObjectType

from api.community.models import (
    Article,
    Company,
    CompanyRevision,
    Comment,
    Hashtag,
    Post,
    Thread,
)
from api.users.models import Profile


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article
        fields = ("url",)


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = "__all__"


class CompanyType(DjangoObjectType):
    clap_count = graphene.Int()
    thread_size = graphene.Int()

    class Meta:
        model = Company
        fields = "__all__"

    def resolve_clap_count(self, info):
        return self.clap_count

    def resolve_thread_size(self, info):
        return self.thread_size


class CompanyRevisionType(DjangoObjectType):
    class Meta:
        model = CompanyRevision
        fields = "__all__"


class HashtagType(DjangoObjectType):
    class Meta:
        model = Hashtag
        fields = ("slug",)


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = "__all__"


class ProfileType(DjangoObjectType):
    name = graphene.String()

    def resolve_name(self, info):
        return self.user.name

    class Meta:
        model = Profile
        fields = "__all__"


class ThreadType(DjangoObjectType):
    class Meta:
        model = Thread
        fields = "__all__"
