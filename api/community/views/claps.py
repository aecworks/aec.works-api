from rest_framework import (
    generics,
    serializers,
    permissions,
)
from rest_framework.response import Response

from api.common.exceptions import ErrorsMixin
from api.common.utils import inline_serializer
from api.users.serializers import ProfileSerializer
from .. import models, selectors


class CompanyClapResponseSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    company = inline_serializer(
        fields={
            "name": serializers.CharField(),
            "slug": serializers.CharField(),
            "logo_url": serializers.URLField(),
        }
    )

    class Meta:
        model = models.Comment
        fields = ["profile", "company"]


class CompanyClapsListView(ErrorsMixin, generics.GenericAPIView):
    serializer_class = CompanyClapResponseSerializer
    expected_exceptions = {}
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        profile = self.request.query_params.get("profile")
        qs = selectors.get_company_claps()
        return qs if not profile else qs.filter(profile__slug=profile)

    def get(self, request):
        serializer = CompanyClapResponseSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)
