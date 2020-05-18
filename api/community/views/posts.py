from rest_framework import mixins, generics
from rest_framework import serializers
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api.common.utils import inline_serializer
from api.common.exceptions import ErrorsMixin

from .. import models, selectors, services


class OutPostSerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    profile = inline_serializer(
        fields={"name": serializers.CharField(), "id": serializers.IntegerField()}
    )
    # Annotated Values
    clap_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()

    # def get_comment_count(self, obj):
    #     return sum(
    #         [c.get_descendant_count() for c in obj.comment_thread.comments.all()]
    #     )

    class Meta:
        model = models.Post
        exclude = ["clappers", "slug"]


class PostListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = OutPostSerializer
    queryset = selectors.get_posts_with_comment_count()
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

    def get(self, request, pk):
        return super().retrieve(request, pk)


class PostClapView(ErrorsMixin, generics.GenericAPIView):
    serializer_class = OutPostSerializer
    queryset = selectors.get_posts()
    expected_exceptions = {}

    def post(self, request, pk):
        post = self.get_object()
        result = services.post_clap(post=post, user=request.user)
        return Response(result)
