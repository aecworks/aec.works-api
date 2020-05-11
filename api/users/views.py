from rest_framework import mixins, generics
from rest_framework import serializers
from rest_framework.pagination import LimitOffsetPagination

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.SerializerMethodField()

    def get_email(self, obj):
        return obj.user.email

    class Meta:
        model = Profile
        exclude = ["user", "id"]


class ProfileListView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    pagination_class = LimitOffsetPagination
    page_size = 100

    def get(self, request):
        return super().list(request)
