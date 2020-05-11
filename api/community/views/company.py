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
            "name",
            "slug",
            "description",
            "website",
            "founded_date",
            "twitter_handle",
            "crunchbase_id",
            "employee_count",
            "logo",
            "hashtags",
            # "clappers",
            "root_comment",
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
