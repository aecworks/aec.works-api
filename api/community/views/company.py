import logging

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.http import condition
from rest_framework import generics, mixins, permissions, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.common.exceptions import ErrorsMixin
from api.permissions import IsEditorPermission, IsReadOnly
from api.users.serializers import ProfileSerializer

from .. import annotations, caching, choices, exceptions, models, selectors, services
from .company_articles import ResponseArticleSerializer
from .company_revisions import CompanyRevisionSerializer

logger = logging.getLogger(__name__)


class ResponseCompanySerializer(serializers.ModelSerializer):

    thread_size = serializers.IntegerField(source="thread.size")
    user_did_clap = serializers.BooleanField(default=False)

    articles = ResponseArticleSerializer(many=True)
    current_revision = CompanyRevisionSerializer()

    class Meta:
        model = models.Company
        fields = [
            "slug",
            "thread_id",
            "created_at",
            "clap_count",
            "current_revision",
            "articles",
            "updated_at",
            "status",
            "thread_size",
            "user_did_clap",
        ]


class ResponseCompanyDetailSerializer(ResponseCompanySerializer):
    created_by = ProfileSerializer()

    class Meta:
        model = models.Company
        fields = ["created_by"] + ResponseCompanySerializer.Meta.fields


class RequestCompanySerializer(serializers.Serializer):
    current_revision = CompanyRevisionSerializer()


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

    @method_decorator(cache_control(max_age=60))
    @method_decorator(condition(last_modified_func=caching.company_last_modified))
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
    permission_classes = [permissions.IsAuthenticated | IsReadOnly]

    def get_queryset(self):
        user = self.request.user
        qs = selectors.get_companies()
        if user.is_authenticated:
            qs = annotations.annotate_company_claps(qs, profile_id=user.profile.id)

        q_search = self.request.query_params.get("search")
        q_status = self.request.query_params.get(
            "status", choices.ModerationStatus.REVIEWED.name
        )
        q_hashtags = self.request.query_params.get("hashtags")
        hashtag_names = services.parse_hashtag_query(q_hashtags)

        qs = selectors.filter_companies(qs, q_search, hashtag_names, q_status)

        # /companies/?sort=claps
        sort_query = self.request.query_params.get("sort")
        sort_query_map = {
            # user facin query: field name
            "name": "name",  # default alfa
            "claps": "-clap_count",  # default: hight to low
            "updated": "-updated_at",  # default: oldest to newest
            "location": "location",  # default: alfa
        }
        default = "-updated_at"
        sort_by = sort_query_map.get(sort_query, default)
        # provide ?reverse=1 to revert sorting
        if self.request.query_params.get("reverse"):
            return qs.order_by(sort_by).reverse()
        else:
            return qs.order_by(sort_by)

    @method_decorator(cache_control(max_age=0))
    @method_decorator(condition(last_modified_func=caching.company_list_last_modified))
    def get(self, request):
        """ Get Company List - matches 'ListModelMixin' for pagination"""
        return super().list(request)

    def post(self, request):
        """ Creates New Company """

        profile = request.user.profile

        if not services.can_create_company(profile):
            raise exceptions.TooManyPendingReviews()

        serializer = RequestCompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        raise NotImplementedError("refactoring")
        # hashtag_names = serializer.validated_data.pop("hashtags")
        # attributes = services.CompanyAttributes(
        #     status=choices.CompanyStatus.SUBMITTED.name, **serializer.validated_data
        # )
        # company = services.create_company(
        #     profile=profile, attributes=attributes, hashtag_names=hashtag_names
        # )
        # return Response(ResponseCompanySerializer(company).data)

