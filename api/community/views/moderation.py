import logging

from rest_framework import generics, serializers
from rest_framework.response import Response

from api.common.exceptions import ErrorsMixin
from api.permissions import IsEditorPermission, IsReadOnly

from .. import choices, selectors, services
from .company import ResponseCompanyDetailSerializer
from .company_revisions import ResponseDetailCompanyRevisionSerializer

logger = logging.getLogger(__name__)


class ModerationSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[c.name for c in choices.ModerationStatus])


class CompanyModerateView(ErrorsMixin, generics.GenericAPIView):
    queryset = selectors.get_companies(prefetch=False)
    lookup_field = "slug"
    expected_exceptions = {}
    permission_classes = [IsEditorPermission | IsReadOnly]
    serializer_class = None

    def post(self, request, slug):
        """ Moderates View"""

        serializer = ModerationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        status = serializer.validated_data["status"]
        company = self.get_object()
        profile = request.user.profile

        company = services.moderate_company(
            company=company, profile=profile, status=status
        )
        return Response(ResponseCompanyDetailSerializer(company).data)


class CompanyRevisionModerateView(ErrorsMixin, generics.GenericAPIView):
    queryset = selectors.get_revisions()
    lookup_field = "id"
    expected_exceptions = {}
    permission_classes = [IsEditorPermission | IsReadOnly]
    serializer_class = None

    def post(self, request, id):
        """ Moderates View"""

        serializer = ModerationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        status = serializer.validated_data["status"]
        revision = self.get_object()
        profile = request.user.profile

        revision = services.moderate_revision(
            revision=revision, profile=profile, status=status
        )
        return Response(ResponseDetailCompanyRevisionSerializer(revision).data)
