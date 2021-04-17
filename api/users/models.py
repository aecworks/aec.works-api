from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_extensions.db.fields import AutoSlugField

from api.common.mixins import ReprMixin

from .choices import UserProviderChoices


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Email field is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class User(ReprMixin, AbstractUser):
    email = models.EmailField(unique=True)
    provider = models.CharField(
        max_length=16,
        choices=[(c.name, c.value) for c in UserProviderChoices],
        default=UserProviderChoices.SIGN_UP.name,
    )
    name = models.CharField(max_length=255, null=False, blank=True, default="")

    # Not in use:
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(ReprMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from="user__name")
    # Optional
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=64, blank=True, null=True)
    twitter = models.CharField(max_length=15, null=True, blank=True)
    github = models.CharField(max_length=40, null=True, blank=True)
    avatar = models.ForeignKey(
        "images.ImageAsset", on_delete=models.PROTECT, null=True, blank=True
    )

    @property
    def email(self):
        return self.user.email

    @property
    def name(self):
        return self.user.name

    def __str__(self):
        return f"<Profile user={self.user.email}>"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
