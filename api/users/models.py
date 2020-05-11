from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.common.mixins import ReprMixin


class User(ReprMixin, AbstractUser):
    pass


class Profile(ReprMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Optional
    bio = models.TextField(blank=True, null=True)
    twitter = models.CharField(max_length=15, null=True, blank=True)
    location = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"<Profile user={self.user.username}>"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Not sure this is needed?
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
