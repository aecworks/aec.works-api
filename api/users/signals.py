# from django.conf import settings
# from django.contrib.auth.models import AuthConfig, Permission
# from django.contrib.contenttypes.models import ContentType
# from django.db.models.signals import post_init
# from django.dispatch import receiver

# from api.users.groups import groups_permissions
# from api.users.services import create_group_and_permissions


# @receiver(pre_migrate, sender=AuthConfig)
# def setup_user_groups(sender, **kwargs):
#     create_group_and_permissions(groups_permissions)
