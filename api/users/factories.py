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
        from api.images.factories import ImageAssetFactory

        obj.avatar = ImageAssetFactory(created_by=obj)
        obj.save()
