from rest_framework import generics, permissions, serializers
from rest_framework.response import Response

from api.common.exceptions import ErrorsMixin

from .. import selectors, services


class CompanyClapResponseSerializer(serializers.Serializer):
    name = serializers.CharField(source="company.name")
    slug = serializers.CharField(source="company.slug")


class CompanyProfileClapsListView(ErrorsMixin, generics.GenericAPIView):
    serializer_class = CompanyClapResponseSerializer
    expected_exceptions = {}
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        profile = self.kwargs["profile"]
        return selectors.get_company_claps().filter(profile__slug=profile)

    def get(self, request, profile):
        serializer = CompanyClapResponseSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class CompanyClapView(ErrorsMixin, generics.GenericAPIView):
    queryset = selectors.get_companies(prefetch=False)
    lookup_field = "slug"
    expected_exceptions = {}
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        """ Adds User as Clapper of Company """
        company = self.get_object()
        profile = request.user.profile
        result = services.company_clap(company=company, profile=profile)
        return Response(result)
