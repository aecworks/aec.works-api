from faker import Faker
import factory
from django.db.models.signals import post_save
from . import models

faker = Faker()


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    email = factory.Faker("email")
    name = factory.Faker("name")

    profile = factory.RelatedFactory("api.users.factories.ProfileFactory", "user")


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Profile
        django_get_or_create = ("user",)

    location = factory.Faker("city")
    bio = factory.Faker("text")
    twitter = factory.LazyAttribute(lambda n: faker.user_name()[:15])

    user = factory.SubFactory(UserFactory, profile=None)
