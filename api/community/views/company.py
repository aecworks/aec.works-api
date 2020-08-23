from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import (
    mixins,
    generics,
    serializers,
    permissions,
    filters,
    exceptions,
)
from drf_extra_fields.fields import Base64ImageField


from api.common.exceptions import ErrorsMixin
from api.users.serializers import ProfileSerializer
from .. import models, selectors, services


class ResponseCompanySerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="slug"
    )
    clap_count = serializers.IntegerField(default=None)
    thread_size = serializers.IntegerField(default=None)
    created_by = ProfileSerializer()

    class Meta:
        model = models.Company
        fields = [
            "slug",
            "created_by",
            "thread",
            "created_at",
            "clap_count",
            "thread_size",
            *services.updatable_attributes,
        ]


class ResponseCompanyRevisionSerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="slug"
    )
    company = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    approved_by = ProfileSerializer()
    created_by = ProfileSerializer()

    class Meta:
        model = models.CompanyRevision
        fields = [
            "id",
            "approved_by",
            "created_by",
            "created_at",
            "company",
            *services.updatable_attributes,
        ]


class RequestCompanySerializer(serializers.ModelSerializer):
    hashtags = serializers.ListField(child=serializers.CharField(min_length=1))
    logo = Base64ImageField()
    # cover = Base64ImageField()

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
            "logo",
            # "cover",
        ]


class RequestCompanyRevisionSerializer(serializers.ModelSerializer):
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
            # "cover",
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    search_fields = ["name", "description"]
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        if hashtag_slug := self.request.query_params.get("hashtag"):
            return self.queryset.filter(hashtags__slug__iexact=hashtag_slug)
        return self.queryset.order_by("name")

    def get(self, request):
        return super().list(request)

    # For multipart parser only
    # parser_classes = [MultiPartParser]
    # accepts json

    def post(self, request):
        serializer = RequestCompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = services.create_company(
            profile=request.user.profile, validated_data=serializer.validated_data,
        )
        return Response(ResponseCompanySerializer(company).data)


class CompanyRevisionListView(
    ErrorsMixin, mixins.RetrieveModelMixin, generics.GenericAPIView
):
    serializer_class = ResponseCompanySerializer
    queryset = selectors.get_companies()
    expected_exceptions = {}
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, slug):
        company = self.get_object()
        return Response(
            ResponseCompanyRevisionSerializer(company.revisions.all(), many=True).data
        )

    def post(self, request, slug):
        serializer = RequestCompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = self.get_object()
        revision = services.create_revision(
            company=company,
            profile=request.user.profile,
            validated_data=serializer.validated_data,
        )
        return Response(ResponseCompanyRevisionSerializer(revision).data)


class CompanyRevisionDetailView(ErrorsMixin, generics.GenericAPIView):
    serializer_class = ResponseCompanySerializer
    queryset = selectors.get_revisions()
    expected_exceptions = {}
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, id, action):
        if action == "approve":
            revision = self.get_object()
            if revision.approved_by:
                raise exceptions.NotAcceptable()

            services.apply_revision(revision=revision, profile=request.user.profile)
            return Response(ResponseCompanyRevisionSerializer(revision).data)
        else:
            return Response(status=404)
