import logging

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.http import condition
from rest_framework import generics, mixins, permissions, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.common.exceptions import ErrorsMixin
from api.permissions import IsEditorPermission, IsReadOnly
from api.users.serializers import ProfileSerializer

from .. import annotations, caching, models, selectors, services

logger = logging.getLogger(__name__)


class RequestArticleSerializer(serializers.Serializer):
    url = serializers.CharField(required=True)


class ResponseArticleSerializer(serializers.Serializer):
    url = serializers.CharField(required=True)
    opengraph_data = serializers.JSONField()


class ResponseCompanySerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="slug"
    )
    thread_size = serializers.IntegerField(source="thread.size")
    clap_count = serializers.IntegerField()
    user_did_clap = serializers.BooleanField(default=False)
    articles = ResponseArticleSerializer(many=True)
    cover_url = serializers.SerializerMethodField()
    logo_url = serializers.SerializerMethodField()

    def get_cover_url(self, obj):
        try:
            return obj.cover.file.crop["800x400"].url if obj.cover else None
        except KeyError:
            logger.error(f"failed to cover image for: {obj}")

    def get_logo_url(self, obj):
        try:
            return obj.logo.file.crop["80x80"].url if obj.logo else None
        except KeyError:
            logger.error(f"failed to logo image for: {obj}")

    class Meta:
        model = models.Company
        fields = [
            "slug",
            "thread_id",
            "created_at",
            "clap_count",
            "user_did_clap",
            "thread_size",
            "last_revision_id",
            "articles",
            "logo_url",
            "cover_url",
            "banner",
            "updated_at",
            *services.updatable_attributes,
        ]


class ResponseCompanyDetailSerializer(ResponseCompanySerializer):
    created_by = ProfileSerializer()

    class Meta:
        model = models.Company
        fields = ["created_by"] + ResponseCompanySerializer.Meta.fields


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
        try:
            return obj.cover.file.crop["800x400"].url if obj.cover else None
        except KeyError:
            logger.error(f"failed to cover image for: {obj}")

    def get_logo_url(self, obj):
        try:
            return obj.logo.file.crop["80x80"].url if obj.logo else None
        except KeyError:
            logger.error(f"failed to logo image for: {obj}")

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
    serializer_class = ResponseCompanyDetailSerializer
    queryset = selectors.get_companies()
    expected_exceptions = {}
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        qs = selectors.get_companies().select_related(
            "created_by__avatar", "created_by__user"
        )
        if user.is_authenticated:
            qs = annotations.annotate_company_claps(qs, profile_id=user.profile.id)
        return qs

    def get(self, request, slug):
        return super().retrieve(request, slug)


class CompanyListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    """
    eg. /community/companies/?search=web&hashtags=software
    """

    serializer_class = ResponseCompanySerializer
    queryset = selectors.get_companies()
    pagination_class = PageNumberPagination
    page_size = 10
    expected_exceptions = {}
    permission_classes = [IsEditorPermission | IsReadOnly]

    def get_queryset(self):
        user = self.request.user
        qs = selectors.get_companies()
        if user.is_authenticated:
            qs = annotations.annotate_company_claps(qs, profile_id=user.profile.id)

        query = self.request.query_params.get("search")
        hashtag_names = []

        if hashtag_query := self.request.query_params.get("hashtags"):
            hashtag_names = services.parse_hashtag_query(hashtag_query)

        qs = selectors.query_companies(qs, query, hashtag_names)

        # /companies/?sort=claps
        sort_query = self.request.query_params.get("sort")
        sort_query_map = {
            # user facin query: field name
            "name": "name",  # default alfa
            "claps": "-clap_count",  # default: hight to low
            "updated": "-updated_at",  # default: oldest to newest
            "location": "location",  # default: alfa
        }
        sort_by = sort_query_map.get(sort_query, "name")
        # provide ?reverse=1 to revert sorting
        if self.request.query_params.get("reverse"):
            return qs.order_by(sort_by).reverse()
        else:
            return qs.order_by(sort_by)

    @method_decorator(condition(last_modified_func=caching.company_last_modified))
    @method_decorator(cache_page(3600, key_prefix=caching.CachePrefix.COMPANY_LIST))
    def get(self, request):
        """ Get Company List - matches 'ListModelMixin' for pagination"""
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
