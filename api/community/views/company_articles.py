import logging

from rest_framework import generics, permissions, serializers
from rest_framework.response import Response

from api.common.exceptions import ErrorsMixin

from .. import selectors, services

logger = logging.getLogger(__name__)


class RequestArticleSerializer(serializers.Serializer):
    url = serializers.CharField(required=True)


class ResponseArticleSerializer(serializers.Serializer):
    url = serializers.CharField(required=True)
    opengraph_data = serializers.JSONField()


class CompanyArticleListView(ErrorsMixin, generics.GenericAPIView):
    queryset = selectors.get_companies()
    lookup_field = "slug"
    expected_exceptions = {}
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        """Adds article to a company"""
        serializer = RequestArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        company = self.get_object()
        profile = request.user.profile
        url = serializer.validated_data["url"]

        article = services.create_company_article(
            company=company, url=url, profile=profile
        )

        return Response(ResponseArticleSerializer(article).data)
