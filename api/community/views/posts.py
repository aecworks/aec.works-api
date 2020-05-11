from rest_framework import mixins, generics
from rest_framework import serializers
from rest_framework.pagination import LimitOffsetPagination

from api.common.utils import inline_serializer
from api.common.exceptions import ErrorsMixin
from .. import models, selectors


class OutPostSerializer(serializers.ModelSerializer):
    claps = serializers.IntegerField()
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = models.Post
        # fields = "__all__"
        exclude = ["clappers", "slug"]


class PostListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = OutPostSerializer
    queryset = selectors.get_posts()
    pagination_class = LimitOffsetPagination
    page_size = 50
    expected_exceptions = {}

    def get(self, request):
        return super().list(request)
