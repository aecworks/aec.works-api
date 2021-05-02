import factory
from faker import Faker

from api.common.utils import slugify

from . import choices, models


class CompanyFactory(factory.django.DjangoModelFactory):
    """
    Usage:

        >>> hashtag = f.HashtagFactory(slug="XXX")
        >>> c = f.CompanyFactory(
                current_revision__twitter="XXX",
                current_revision__hashtags=[hashtag]
            )
    """

    slug = factory.LazyAttribute(lambda o: slugify(Faker().company()))
    created_by = factory.SubFactory("api.users.factories.ProfileFactory")
    status = choices.ModerationStatus.UNMODERATED.name

    @factory.post_generation
    def current_revision(obj, created, extracted, **current_revision_kwargs):
        # Only creates revision if at least one arg is provided
        if current_revision_kwargs:
            obj.current_revision = CompanyRevisionFactory(
                company=obj, **current_revision_kwargs
            )
            obj.save()

    class Meta:
        model = models.Company

    class Params:
        duration = 5


class CompanyRevisionFactory(factory.django.DjangoModelFactory):

    created_by = factory.SubFactory("api.users.factories.ProfileFactory")

    name = factory.LazyAttribute(lambda o: o.company.slug.title().replace("-", " "))
    description = factory.Faker("paragraph", nb_sentences=2)

    website = factory.Faker("url")
    twitter = factory.LazyAttribute(lambda o: o.name.lower().replace(" ", "")[:14])
    crunchbase_id = factory.LazyAttribute(lambda o: o.twitter)

    logo = factory.SubFactory("api.images.factories.ImageAssetFactory")
    cover = factory.SubFactory("api.images.factories.ImageAssetFactory")

    hashtags = []

    class Meta:
        model = models.CompanyRevision

    @factory.post_generation
    def hashtags(obj, created, extracted, **kwargs):
        if extracted:
            obj.hashtags.set(extracted)


class HashtagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Hashtag
        django_get_or_create = ("slug",)

    slug = factory.Faker("word")


class ThreadFactory(factory.django.DjangoModelFactory):

    comments = factory.RelatedFactory(
        "api.community.factories.CommentFactory", factory_related_name="thread"
    )

    class Meta:
        model = models.Thread


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Comment

    text = factory.Faker("paragraph")
    profile = factory.SubFactory("api.users.factories.ProfileFactory")
    thread = factory.SubFactory("api.community.factories.ThreadFactory")
