from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import (
    mixins,
    generics,
    serializers,
    permissions,
    # filters,
)


from api.common.exceptions import ErrorsMixin
from api.users.serializers import ProfileSerializer
from .. import models, selectors, services


class ResponseCompanySerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="slug"
    )
    clap_count = serializers.IntegerField(default=0)
    thread_size = serializers.IntegerField(default=0)
    created_by = ProfileSerializer()
    thread_id = serializers.IntegerField()

    class Meta:
        model = models.Company
        fields = [
            "slug",
            "created_by",
            "thread_id",
            "created_at",
            "clap_count",
            "thread_size",
            "last_revision_id",
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
            "applied",
            "approved_by",
            "created_by",
            "created_at",
            "company",
            *services.updatable_attributes,
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
            "logo_url",
            "cover_url",
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
            "logo_url",
            "cover_url",
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
    """
    eg. /community/companies/?search=web&hashtags=software
    """

    serializer_class = ResponseCompanySerializer
    queryset = selectors.get_companies()
    pagination_class = LimitOffsetPagination
    page_size = 25
    expected_exceptions = {}
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # search_fields = ["name", "description"]
    # filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        query = self.request.query_params.get("search")
        hashtag_names = []

        if hashtag_query := self.request.query_params.get("hashtags"):
            hashtag_names = services.parse_hashtag_query(hashtag_query)

        return selectors.query_companies(query, hashtag_names).order_by("name")

    def get(self, request):
        """ Get Company List """
        return super().list(request)

    def post(self, request):
        """ Creates New Company """
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
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    expected_exceptions = {}

    def get(self, request, slug):
        company = self.get_object()
        return Response(
            ResponseCompanyRevisionSerializer(
                company.revisions.all().order_by("-created_at"), many=True
            ).data
        )

    def post(self, request, slug):
        """ Creates New Company Revision """
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
        if action == "approve":  # approve
            revision = self.get_object()
            # TODO: rethink approved_by, applied by
            # or diff model Revision.diffs = [{"field": "name", op: "delete"}]
            # if revision.approved_by:
            # raise exceptions.ValidationError("Revision is already approved")

            services.apply_revision(revision=revision, profile=request.user.profile)
            return Response(ResponseCompanyRevisionSerializer(revision).data)
        else:
            return Response(status=404)


class CompanyClapView(ErrorsMixin, generics.GenericAPIView):
    queryset = selectors.get_companies()
    expected_exceptions = {}
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        """ Adds User as Clapper of Company """
        company = self.get_object()
        profile = request.user.profile
        result = services.company_clap(company=company, profile=profile)
        return Response(result)
