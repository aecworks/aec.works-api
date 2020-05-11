# from api.common.utils import to_slug
# from .choices import EmployeeCountChoices
import factory
from . import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Faker("user_name")
    email = factory.Faker("email")


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Profile
        django_get_or_create = ("user",)

    twitter = factory.Faker("user_name")
    location = factory.Faker("city")
    user = factory.SubFactory(UserFactory)
