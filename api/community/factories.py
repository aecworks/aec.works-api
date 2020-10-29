import factory
from . import models


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Company

    name = factory.Faker("company")
    # slug - use signal
    description = factory.Faker("paragraph", nb_sentences=2)
    created_by = factory.SubFactory("api.users.factories.ProfileFactory")

    website = factory.Faker("url")
    twitter = factory.LazyAttribute(lambda o: o.name.lower().replace(" ", "")[:14])
    crunchbase_id = factory.LazyAttribute(lambda o: o.twitter)

    logo = factory.SubFactory("api.images.factories.ImageAssetFactory")
    cover = factory.SubFactory("api.images.factories.ImageAssetFactory")
    # clappers
    # thread
    # created_at
    # c
    # replaced_by
    # approved_by

    @factory.post_generation
    def post(obj, *args, **kwargs):
        obj.hashtags.add(HashtagFactory())


class CompanyRevisionFactory(factory.django.DjangoModelFactory):
    created_by = factory.SubFactory("api.users.factories.ProfileFactory")
    applied = False

    class Meta:
        model = models.CompanyRevision


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
