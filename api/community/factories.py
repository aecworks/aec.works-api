# from .choices import EmployeeCountChoices
# from api.common.utils import to_slug
import factory
from . import models


class Company(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Company

    name = factory.Faker("company")
    # slug
    description = factory.Faker("paragraph", nb_sentences=2)
    website = factory.Faker("url")
    founded_date = factory.Faker("date")
    twitter_handle = factory.LazyAttribute(
        lambda o: o.name.lower().replace(" ", "")[:14]
    )
    crunchbase_id = factory.LazyAttribute(lambda o: o.twitter_handle)
    # employee_count
    # logo
    # hashtags
    # clappers
    # comment_thread
    # created_at
    # revision_of
    # replaced_by
    # approved_by
    # editor


class Hashtag(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Hashtag

    name = factory.Faker("word")


class Post(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Post

    body = factory.Faker("text", max_nb_chars=1000)
    title = factory.Faker("sentence")
    comment_thread = None
    profile = factory.SubFactory("api.users.factories.ProfileFactory")
    # companies = []
    # hashtags = []
    # clappers = []
    # created_at
    # updated_at


class CommentThread(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CommentThread


class Comment(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Comment

    text = factory.Faker("paragraph")
    profile = factory.SubFactory("api.users.factories.ProfileFactory")
    # parent
    # clappers
    # created_at

