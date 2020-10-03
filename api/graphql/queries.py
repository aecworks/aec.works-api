import graphene

from api import community
from . import types as t


class CommentQuery:
    comments_by_thread_id = graphene.List(
        t.CommentType, thread_id=graphene.Int(required=True)
    )
    comments_by_parent_id = graphene.List(
        t.CommentType, parent_id=graphene.Int(required=True)
    )

    def resolve_comments_by_thread_id(root, info, thread_id):
        return community.selectors.get_thread_comments(thread_id=thread_id).all()

    def resolve_comments_by_parent_id(root, info, parent_id):
        return community.selectors.get_comment_children(parent_id=parent_id).all()


class CompanyQuery:
    companies = graphene.List(
        t.CompanyType, hashtag_names=graphene.List(graphene.String)
    )
    company_by_slug = graphene.Field(t.CompanyType, slug=graphene.String())

    def resolve_companies(root, info, filter="", hashtag_names=None):
        qs = community.selectors.get_companies()
        return community.selectors.query_companies(qs, filter, hashtag_names).order_by(
            "name"
        )

    def resolve_company_by_slug(root, info, slug):
        return community.models.Company.objects.filter(slug=slug).first()


class HashtagQuery:
    hashtags = graphene.List(t.HashtagType)

    def resolve_hashtags(root, info):
        return community.models.Hashtag.objects.all()


class PostQuery:
    posts = graphene.List(
        t.PostType,
        hashtag_names=graphene.List(graphene.String),
        filter=graphene.String(),
    )

    def resolve_posts(root, info, hashtag_names=None, filter=""):
        qs = community.selectors.get_posts()
        return community.selectors.query_posts(qs, filter, hashtag_names).order_by(
            "-hot_datetime", "created_at", "slug"
        )

    post_by_slug = graphene.Field(t.PostType, slug=graphene.String(required=True))

    def resolve_post_by_slug(root, info, slug):
        return community.models.Post.objects.filter(slug=slug).first()


class Query(graphene.ObjectType, CommentQuery, CompanyQuery, HashtagQuery, PostQuery):
    ...
