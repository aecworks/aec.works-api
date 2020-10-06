from django.core.exceptions import PermissionDenied
from rest_framework import mixins, generics, serializers, permissions
from rest_framework import exceptions as drf_exceptions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api.common.exceptions import ErrorsMixin
from api.users.serializers import ProfileSerializer
from .. import models, selectors, services


class PostListSerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="slug"
    )
    profile = ProfileSerializer()
    clap_count = serializers.IntegerField()
    thread_size = serializers.IntegerField()
    thread_id = serializers.IntegerField()
    banner = serializers.CharField(source="get_banner_display")
    cover_img_url = serializers.SerializerMethodField()

    def get_cover_img_url(self, obj):
        return obj.cover_img.file.url if obj.cover_img else None

    class Meta:
        model = models.Post
        fields = [
            "hashtags",
            "profile",
            "title",
            "body",
            "clap_count",
            "thread_size",
            "thread_id",
            "slug",
            "banner",
            "cover_img_url",
        ]


class NewPostRequestSerializer(serializers.ModelSerializer):
    hashtags = serializers.ListField(child=serializers.CharField(min_length=1))

    class Meta:
        model = models.Post
        fields = ["hashtags", "title", "body"]


class NewPostResponseSerializer(serializers.ModelSerializer):
    thread_id = serializers.IntegerField(read_only=True)
    slug = serializers.CharField(read_only=True)
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="slug"
    )
    banner = serializers.CharField(source="get_banner_display")
    cover_img_url = serializers.SerializerMethodField()

    def get_cover_img_url(self, obj):
        return obj.cover_img.file.url if obj.cover_img else None

    class Meta:
        model = models.Post
        fields = [
            "hashtags",
            "title",
            "body",
            "thread_id",
            "slug",
            "banner",
            "cover_img_url",
        ]


class PostListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = PostListSerializer
    queryset = selectors.get_posts()
    pagination_class = LimitOffsetPagination
    page_size = 50
    expected_exceptions = {}
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        query = self.request.query_params.get("search")
        hashtag_names = []

        if hashtag_query := self.request.query_params.get("hashtags"):
            hashtag_names = services.parse_hashtag_query(hashtag_query)

        return selectors.query_posts(self.queryset, query, hashtag_names).order_by(
            "-hot_datetime", "created_at", "slug"
        )

    def get(self, request):
        return super().list(request)

    def post(self, request):
        serializer = NewPostRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = services.create_post(
            profile=request.user.profile,
            title=serializer.validated_data["title"],
            body=serializer.validated_data["body"],
            hashtag_names=serializer.validated_data["hashtags"],
        )
        return Response(NewPostResponseSerializer(post).data, status=201)


class PostDetailView(
    ErrorsMixin, mixins.RetrieveModelMixin, generics.GenericAPIView,
):
    serializer_class = PostListSerializer
    queryset = selectors.get_posts()
    expected_exceptions = {}
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    expected_exceptions = {PermissionDenied: drf_exceptions.PermissionDenied}

    def get(self, request, slug):
        return super().retrieve(request, slug)

    def patch(self, request, slug):
        serializer = NewPostRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = services.update_post(
            slug=slug,
            profile=request.user.profile,
            title=serializer.validated_data["title"],
            body=serializer.validated_data["body"],
            hashtag_names=serializer.validated_data["hashtags"],
        )
        return Response(NewPostResponseSerializer(post).data, status=200)


class PostClapView(ErrorsMixin, generics.GenericAPIView):
    serializer_class = PostListSerializer
    queryset = selectors.get_posts()
    expected_exceptions = {}
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        post = self.get_object()
        profile = request.user.profile
        result = services.post_clap(post=post, profile=profile)
        return Response(result)
