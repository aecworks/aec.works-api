from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.CharField(source="avatar")

    class Meta:
        model = Profile
        fields = ["slug", "name", "avatar_url"]


class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ["user"]
