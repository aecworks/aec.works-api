from rest_framework import mixins, generics
from rest_framework import serializers
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.common.utils import inline_serializer
from api.common.exceptions import ErrorsMixin

from .. import models, selectors, services


class OutPostSerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="slug"
    )
    profile = inline_serializer(
        fields={"name": serializers.CharField(), "id": serializers.IntegerField()}
    )
    clap_count = serializers.IntegerField()
    thread_size = serializers.IntegerField()

    class Meta:
        model = models.Post
        exclude = ["clappers"]


class PostListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = OutPostSerializer
    queryset = selectors.get_posts()
    pagination_class = LimitOffsetPagination
    page_size = 50
    expected_exceptions = {}

    def get_queryset(self):
        if hashtag_name := self.request.query_params.get("hashtag"):
            return self.queryset.filter(hashtags__name__contains=hashtag_name)
        return self.queryset

    def get(self, request):
        return super().list(request)


class PostDetailView(ErrorsMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = OutPostSerializer
    queryset = selectors.get_posts()
    expected_exceptions = {}
    lookup_field = "slug"

    def get(self, request, slug):
        return super().retrieve(request, slug)


class PostClapView(ErrorsMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OutPostSerializer
    queryset = selectors.get_posts()
    expected_exceptions = {}
    lookup_field = "slug"

    def post(self, request, slug):
        post = self.get_object()
        result = services.post_clap(post=post, user=request.user)
        return Response(result)
