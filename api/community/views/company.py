from rest_framework import mixins, generics, serializers
from rest_framework.pagination import LimitOffsetPagination

from api.common.exceptions import ErrorsMixin
from ..models import Company
from .. import models, selectors


class OutCompanySerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = models.Company
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "website",
            "founded_date",
            "twitter_handle",
            "location",
            "crunchbase_id",
            "employee_count",
            "logo",
            "hashtags",
            # "clappers",
            "comment_thread",
            "created_at",
            "revision_of",
            "replaced_by",
            "approved_by",
            "editor",
        ]
        # exclude = ["clappers"]


class CompanyListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = OutCompanySerializer
    queryset = selectors.get_companies()
    pagination_class = LimitOffsetPagination
    page_size = 50
    expected_exceptions = {}

    def get(self, request):
        return super().list(request)


class CompanyDetailView(
    ErrorsMixin, mixins.RetrieveModelMixin, generics.GenericAPIView
):
    serializer_class = OutCompanySerializer
    queryset = selectors.get_companies()
    expected_exceptions = {}

    def get(self, request, pk):
        return super().retrieve(request, pk)
