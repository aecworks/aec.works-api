import factory
from faker import Faker

from api.common.utils import slugify

from . import choices, models


class CompanyFactory(factory.django.DjangoModelFactory):

    slug = factory.LazyAttribute(lambda o: slugify(Faker().company()))
    created_by = factory.SubFactory("api.users.factories.ProfileFactory")
    status = choices.ModerationStatus.REVIEWED.name
    current_revision = None

    @factory.post_generation
    def post(obj, *args, **kwargs):
        obj.current_revision = CompanyRevisionFactory(company=obj)
        obj.save()

    class Meta:
        model = models.Company

    class Params:
        duration = 5


class CompanyRevisionFactory(factory.django.DjangoModelFactory):

    company = factory.SubFactory("api.community.factories.CompanyFactory",)
    created_by = factory.SubFactory("api.users.factories.ProfileFactory")

    name = factory.LazyAttribute(lambda o: o.company.slug.title().replace("-", " "))
    description = factory.Faker("paragraph", nb_sentences=2)

    website = factory.Faker("url")
    twitter = factory.LazyAttribute(lambda o: o.name.lower().replace(" ", "")[:14])
    crunchbase_id = factory.LazyAttribute(lambda o: o.twitter)

    logo = factory.SubFactory("api.images.factories.ImageAssetFactory")
    cover = factory.SubFactory("api.images.factories.ImageAssetFactory")

    class Meta:
        model = models.CompanyRevision

    @factory.post_generation
    def post(obj, *args, **kwargs):
        obj.hashtags.add(HashtagFactory())


class HashtagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Hashtag
        django_get_or_create = ("slug",)

    slug = factory.Faker("word")


class ThreadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Thread


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Comment

    text = factory.Faker("paragraph")
    profile = factory.SubFactory("api.users.factories.ProfileFactory")
