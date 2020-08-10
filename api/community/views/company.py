from rest_framework import mixins, generics, serializers, permissions, filters
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from api.common.exceptions import ErrorsMixin
from .. import models, selectors, services


class ResponseCompanySerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="slug"
    )
    clap_count = serializers.IntegerField()
    thread_size = serializers.IntegerField()
    employee_count = serializers.SerializerMethodField()

    def get_employee_count(self, obj):
        return obj.get_employee_count_display()

    class Meta:
        model = models.Company
        fields = [
            "name",
            "slug",
            "description",
            "profile",
            "website",
            "founded_date",
            "twitter_handle",
            "location",
            "crunchbase_id",
            "employee_count",
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
    employee_count = serializers.CharField()

    class Meta:
        model = models.Company
        fields = [
            "name",
            "description",
            "website",
            "founded_date",
            "twitter_handle",
            "location",
            "crunchbase_id",
            "employee_count",
            "hashtags",
            # "logo",
        ]


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

    def patch(self, request, slug):
        serializer = RequestCompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = self.get_object()
        updated_company = services.update_company(
            company=company,
            profile=request.user.profile,
            validated_data=serializer.validated_data,
        )
        return Response(ResponseCompanySerializer(updated_company).data)
