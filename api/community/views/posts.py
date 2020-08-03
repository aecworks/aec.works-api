from rest_framework import mixins, generics, serializers, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api.common.utils import inline_serializer
from api.common.exceptions import ErrorsMixin

from .. import models, selectors, services


class PostDetailsSerializer(serializers.ModelSerializer):
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


class NewPostSerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True, slug_field="slug", queryset=models.Hashtag.objects.all()
    )

    thread_id = serializers.IntegerField(read_only=True)
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = models.Post
        fields = ["hashtags", "title", "body", "slug", "thread_id"]


class PostListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = PostDetailsSerializer
    queryset = selectors.get_posts()
    pagination_class = LimitOffsetPagination
    page_size = 50
    expected_exceptions = {}
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if hashtag_slug := self.request.query_params.get("hashtag"):
            return self.queryset.filter(hashtags__slug__contains=hashtag_slug)
        return self.queryset

    def get(self, request):
        return super().list(request)

    def post(self, request):
        serializer = NewPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = services.create_post(
            profile=request.user.profile,
            title=serializer.validated_data["title"],
            body=serializer.validated_data["body"],
            hashtag_names=serializer.validated_data["hashtags"],
        )
        return Response(NewPostSerializer(post).data, status=201)


class PostDetailView(
    ErrorsMixin, mixins.RetrieveModelMixin, generics.GenericAPIView,
):
    serializer_class = PostDetailsSerializer
    queryset = selectors.get_posts()
    expected_exceptions = {}
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, slug):
        return super().retrieve(request, slug)

    def patch(self, request, slug):
        serializer = NewPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = services.update_post(
            slug=slug,
            profile=request.user.profile,
            title=serializer.validated_data["title"],
            body=serializer.validated_data["body"],
            hashtag_names=serializer.validated_data["hashtags"],
        )
        return Response(NewPostSerializer(post).data, status=200)


class PostClapView(ErrorsMixin, generics.GenericAPIView):
    serializer_class = PostDetailsSerializer
    queryset = selectors.get_posts()
    expected_exceptions = {}
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        post = self.get_object()
        profile = request.user.profile
        result = services.post_clap(post=post, profile=profile)
        return Response(result)
