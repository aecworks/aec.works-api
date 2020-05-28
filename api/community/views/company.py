from rest_framework import mixins, generics, serializers
from rest_framework.pagination import LimitOffsetPagination
from api.common.exceptions import ErrorsMixin
from .. import models, selectors


class OutCompanySerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    clap_count = serializers.IntegerField()
    thread_size = serializers.IntegerField()
    employee_count = serializers.SerializerMethodField()

    def get_employee_count(self, obj):
        return obj.get_employee_count_display()

    class Meta:
        model = models.Company
        fields = [
            "id",
            "name",
            "slug",
            "clap_count",
            "thread_size",
            "description",
            "website",
            "founded_date",
            "twitter_handle",
            "location",
            "crunchbase_id",
            "employee_count",
            "logo",
            "hashtags",
            "thread",
            "created_at",
            "revision_of",
            "replaced_by",
            "approved_by",
            "editor",
        ]


class CompanyListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = OutCompanySerializer
    queryset = selectors.get_companies()
    pagination_class = LimitOffsetPagination
    page_size = 25
    expected_exceptions = {}

    def get(self, request):
        return super().list(request)


class CompanyDetailView(
    ErrorsMixin, mixins.RetrieveModelMixin, generics.GenericAPIView
):
    serializer_class = OutCompanySerializer
    queryset = selectors.get_companies()
    expected_exceptions = {}
    lookup_field = "slug"

    def get(self, request, slug):
        return super().retrieve(request, slug)
