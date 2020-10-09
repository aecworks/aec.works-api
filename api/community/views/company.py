from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import (
    mixins,
    generics,
    serializers,
    permissions,
)
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


from api.permissions import IsEditorPermission, IsReadOnly
from api.common.exceptions import ErrorsMixin
from api.users.serializers import ProfileSerializer
from .. import models, selectors, services


class RequestArticleSerializer(serializers.Serializer):
    url = serializers.CharField(required=True)


class ResponseArticleSerializer(serializers.Serializer):
    url = serializers.CharField(required=True)
    opengraph_data = serializers.JSONField()


class ResponseCompanySerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="slug"
    )
    clap_count = serializers.IntegerField(default=0)
    thread_size = serializers.IntegerField(default=0, source="thread.size")
    # created_by = ProfileSerializer()
    thread_id = serializers.IntegerField()
    articles = ResponseArticleSerializer(many=True)
    cover_url = serializers.SerializerMethodField()
    logo_url = serializers.SerializerMethodField()

    def get_cover_url(self, obj):
        return obj.cover.file.crop["800x400"].url if obj.cover else None

    def get_logo_url(self, obj):
        return obj.logo.file.crop["80x80"].url if obj.logo else None

    class Meta:
        model = models.Company
        fields = [
            "slug",
            # "created_by",
            "thread_id",
            "created_at",
            "clap_count",
            "thread_size",
            "last_revision_id",
            "articles",
            "logo_url",
            "cover_url",
            *services.updatable_attributes,
        ]


class ResponseCompanyRevisionSerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="slug"
    )
    company = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    approved_by = ProfileSerializer()
    created_by = ProfileSerializer()
    cover_url = serializers.SerializerMethodField()
    logo_url = serializers.SerializerMethodField()

    def get_cover_url(self, obj):
        return obj.cover.file.crop["800x400"].url if obj.cover else None

    def get_logo_url(self, obj):
        return obj.logo.file.crop["80x80"].url if obj.logo else None

    class Meta:
        model = models.CompanyRevision
        fields = [
            "id",
            "applied",
            "approved_by",
            "created_by",
            "created_at",
            "company",
            "logo_url",
            "cover_url",
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
            "twitter",
            "location",
            "crunchbase_id",
            "hashtags",
            "logo",
            "cover",
        ]


class RequestCompanyRevisionSerializer(serializers.ModelSerializer):
    hashtags = serializers.ListField(child=serializers.CharField(min_length=1))

    class Meta:
        model = models.Company
        fields = [
            "name",
            "description",
            "website",
            "twitter",
            "location",
            "crunchbase_id",
            "hashtags",
            "logo",
            "cover",
        ]


class CompanyDetailView(
    ErrorsMixin, mixins.RetrieveModelMixin, generics.GenericAPIView,
):
    serializer_class = ResponseCompanySerializer
    queryset = selectors.get_companies()
    expected_exceptions = {}
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @method_decorator(cache_page(60 * 60))
    def get(self, request, slug):
        return super().retrieve(request, slug)


class CompanyListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    """
    eg. /community/companies/?search=web&hashtags=software
    """

    serializer_class = ResponseCompanySerializer
    queryset = selectors.get_companies()
    pagination_class = LimitOffsetPagination
    page_size = 10
    expected_exceptions = {}
    permission_classes = [IsEditorPermission | IsReadOnly]

    def get_queryset(self):
        query = self.request.query_params.get("search")
        hashtag_names = []

        if hashtag_query := self.request.query_params.get("hashtags"):
            hashtag_names = services.parse_hashtag_query(hashtag_query)

        return selectors.query_companies(self.queryset, query, hashtag_names).order_by(
            "name"
        )

    @method_decorator(cache_page(60))
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
    permission_classes = [IsEditorPermission | IsReadOnly]
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
    permission_classes = [IsEditorPermission | IsReadOnly]

    def post(self, request, id, action):
        if action == "approve":  # approve
            revision = self.get_object()
            services.apply_revision(revision=revision, profile=request.user.profile)
            return Response(ResponseCompanyRevisionSerializer(revision).data)
        else:
            return Response(status=404)


class CompanyClapView(ErrorsMixin, generics.GenericAPIView):
    queryset = selectors.get_companies()
    lookup_field = "slug"
    expected_exceptions = {}
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        """ Adds User as Clapper of Company """
        company = self.get_object()
        profile = request.user.profile
        result = services.company_clap(company=company, profile=profile)
        return Response(result)


class CompanyArticleListView(ErrorsMixin, generics.GenericAPIView):
    queryset = selectors.get_companies()
    lookup_field = "slug"
    expected_exceptions = {}
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        """ Adds article to a company """
        serializer = RequestArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        company = self.get_object()
        profile = request.user.profile
        url = serializer.validated_data["url"]

        article = services.create_company_article(
            company=company, url=url, profile=profile
        )

        return Response(ResponseArticleSerializer(article).data)
