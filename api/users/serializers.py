from rest_framework import serializers

from .models import Profile
from .services import default_avatar


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    def get_avatar_url(self, obj):
        return obj.avatar.file.url if obj.avatar else default_avatar(obj.email)

    class Meta:
        model = Profile
        fields = ["slug", "name", "avatar_url"]


class ProfileDetailSerializer(serializers.ModelSerializer):
    provider = serializers.SerializerMethodField()
    name = serializers.CharField()
    groups = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()

    def get_avatar_url(self, obj):
        return obj.avatar.file.url if obj.avatar else default_avatar(obj.email)

    def get_provider(self, profile):
        return profile.user.provider

    def get_groups(self, profile):
        return [g.name for g in profile.user.groups.all()]

    class Meta:
        model = Profile
        exclude = ["id", "user"]
