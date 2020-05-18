# from api.common.utils import to_slug
# from .choices import EmployeeCountChoices
import factory
from django.db.models.signals import post_save
from . import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    profile = factory.RelatedFactory("api.users.factories.ProfileFactory", "user")


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Profile

    twitter = factory.Faker("user_name")
    location = factory.Faker("city")
    bio = factory.Faker("text")
    user = factory.SubFactory(UserFactory, profile=None)
