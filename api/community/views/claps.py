from rest_framework import (
    generics,
    serializers,
    permissions,
)
from rest_framework.response import Response
from api.common.exceptions import ErrorsMixin
from .. import selectors


class CompanyClapResponseSerializer(serializers.Serializer):
    name = serializers.CharField(source="company.name")
    slug = serializers.CharField(source="company.slug")
    logo_url = serializers.CharField(source="company.logo_url")


class CompanyClapsListView(ErrorsMixin, generics.GenericAPIView):
    serializer_class = CompanyClapResponseSerializer
    expected_exceptions = {}
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        profile = self.kwargs["profile"]
        return selectors.get_company_claps().filter(profile__slug=profile)

    def get(self, request, profile):
        serializer = CompanyClapResponseSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)
