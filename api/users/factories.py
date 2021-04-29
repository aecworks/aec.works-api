import factory
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from faker import Faker

from api.images.factories import ImageAssetFactory

from . import models

faker = Faker()


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    email = factory.Faker("email")
    name = factory.Faker("name")
    is_active = True

    profile = factory.RelatedFactory("api.users.factories.ProfileFactory", "user")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", None)
        obj = super(UserFactory, cls)._create(model_class, *args, **kwargs)
        # ensure the raw password gets set after the initial save
        obj.set_password(password)
        obj.save()
        return obj

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        # Simple build, do nothing.
        if not create:
            return

        if extracted:
            # A list of groups were passed in, use them
            for group_name in extracted:
                group = GroupFactory(name=group_name)
                self.groups.add(group)


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Profile
        django_get_or_create = ("user",)

    location = factory.Faker("city")
    bio = factory.Faker("text")
    twitter = factory.LazyAttribute(lambda n: faker.user_name()[:15])

    user = factory.SubFactory(UserFactory, profile=None)

    @factory.post_generation
    def post(obj, *args, **kwargs):
        obj.avatar = ImageAssetFactory(created_by=obj)
        obj.save()


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group
        django_get_or_create = ("name",)

    name = "editors"
