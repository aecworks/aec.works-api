from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["slug", "name", "bio", "location", "avatar_url"]


class ProfileDetailSerializer(serializers.ModelSerializer):
    provider = serializers.SerializerMethodField()
    name = serializers.CharField()
    groups = serializers.SerializerMethodField()

    def get_provider(self, profile):
        return profile.user.provider

    def get_groups(self, profile):
        return [g.name for g in profile.user.groups.all()]

    class Meta:
        model = Profile
        exclude = ["id", "user"]
