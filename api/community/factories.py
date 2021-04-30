import factory

from . import models


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Company

    slug = factory.Faker("company")
    created_by = factory.SubFactory("api.users.factories.ProfileFactory")
    current_revision = factory.SubFactory(
        "api.community.factories.CompanyRevisionFactory"
    )


class CompanyRevisionFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("company")
    description = factory.Faker("paragraph", nb_sentences=2)

    website = factory.Faker("url")
    twitter = factory.LazyAttribute(lambda o: o.name.lower().replace(" ", "")[:14])
    crunchbase_id = factory.LazyAttribute(lambda o: o.twitter)

    logo = factory.SubFactory("api.images.factories.ImageAssetFactory")
    cover = factory.SubFactory("api.images.factories.ImageAssetFactory")

    created_by = factory.SubFactory("api.users.factories.ProfileFactory")

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


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Post

    body = factory.Faker("text", max_nb_chars=1000)
    title = factory.Faker("sentence")
    thread = None
    profile = factory.SubFactory("api.users.factories.ProfileFactory")
    # hashtags = []
    # companies = []
    # clappers = []
    # created_at
    # updated_at


class ThreadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Thread


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Comment

    text = factory.Faker("paragraph")
    profile = factory.SubFactory("api.users.factories.ProfileFactory")
