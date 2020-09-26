import graphene
from graphene_django import DjangoObjectType

from api.community import selectors
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


class Query(graphene.ObjectType):
    companies = graphene.List(CompanyType, hashtag=graphene.String(required=False))
    company_by_slug = graphene.Field(CompanyType, slug=graphene.String(required=True))

    posts = graphene.List(PostType)

    def resolve_companies(root, info, hashtag):
        # return Company.objects.filter(hashtags__slug=hashtag)
        return selectors.get_companies().filter(hashtags__slug=hashtag)

    def resolve_company_by_slug(root, info, slug):
        return Company.objects.filter(slug=slug).first()

    def resolve_posts(root, info):
        return Post.objects.all()


schema = graphene.Schema(query=Query)
