from rest_framework import mixins, generics
from rest_framework import serializers
from rest_framework.pagination import LimitOffsetPagination

from api.common.exceptions import ErrorsMixin
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.SerializerMethodField()
    name = serializers.CharField()

    def get_email(self, obj):
        return obj.user.email

    class Meta:
        model = Profile
        exclude = ["user"]


class ProfileListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all().exclude(user__username="dev")
    pagination_class = LimitOffsetPagination
    page_size = 100

    def get(self, request):
        return super().list(request)


class ProfileDetailView(
    ErrorsMixin, mixins.RetrieveModelMixin, generics.GenericAPIView
):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get(self, request, pk):
        return super().retrieve(request, pk)
