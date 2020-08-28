from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["slug", "name", "avatar_url"]


class ProfileDetailSerializer(serializers.ModelSerializer):
    provider = serializers.SerializerMethodField()
    name = serializers.CharField()

    def get_provider(self, profile):
        return profile.user.provider

    class Meta:
        model = Profile
        exclude = ["id", "user"]
