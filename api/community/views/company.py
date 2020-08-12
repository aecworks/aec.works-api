from rest_framework import mixins, generics, serializers, permissions, filters
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from api.common.exceptions import ErrorsMixin
from .. import models, selectors, services


class ResponseCompanySerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="slug"
    )
    clap_count = serializers.IntegerField(default=None)
    thread_size = serializers.IntegerField(default=None)

    class Meta:
        model = models.Company
        fields = [
            "name",
            "slug",
            "description",
            "created_by",
            "website",
            "twitter_handle",
            "location",
            "crunchbase_id",
            "logo",
            "cover",
            "hashtags",
            "thread",
            "created_at",
            "clap_count",
            "thread_size",
        ]


class RequestCompanySerializer(serializers.ModelSerializer):
    hashtags = serializers.ListField(child=serializers.CharField(min_length=1))

    class Meta:
        model = models.Company
        fields = [
            "name",
            "description",
            "website",
            "twitter_handle",
            "location",
            "crunchbase_id",
            "hashtags",
            # "logo",
        ]


class CompanyDetailView(
    ErrorsMixin, mixins.RetrieveModelMixin, generics.GenericAPIView,
):
    serializer_class = ResponseCompanySerializer
    queryset = selectors.get_companies()
    expected_exceptions = {}
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, slug):
        return super().retrieve(request, slug)


class CompanyListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ResponseCompanySerializer
    queryset = selectors.get_companies()
    pagination_class = LimitOffsetPagination
    page_size = 25
    expected_exceptions = {}
    permission_classes = [permissions.AllowAny]

    search_fields = ["name", "description"]
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        if hashtag_slug := self.request.query_params.get("hashtag"):
            return self.queryset.filter(hashtags__slug__iexact=hashtag_slug)
        return self.queryset.order_by("name")

    def get(self, request):
        return super().list(request)

    def post(self, request):
        serializer = RequestCompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = services.create_company(
            profile=request.user.profile, validated_data=serializer.validated_data,
        )
        return Response(ResponseCompanySerializer(company).data)


class CompanyRevisionListView(
    ErrorsMixin, mixins.RetrieveModelMixin, generics.GenericAPIView,
):
    serializer_class = ResponseCompanySerializer
    queryset = selectors.get_companies()
    expected_exceptions = {}
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, slug):
        serializer = RequestCompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = self.get_object()
        updated_company = services.create_revision(
            company=company,
            profile=request.user.profile,
            validated_data=serializer.validated_data,
        )
        return Response(ResponseCompanySerializer(updated_company).data)
