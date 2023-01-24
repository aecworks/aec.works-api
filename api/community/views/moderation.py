import logging

from rest_framework import generics, serializers
from rest_framework.response import Response

from api.common.exceptions import ErrorsMixin
from api.common.utils import validate_or_raise
from api.permissions import IsEditorPermission, IsReadOnly
from api.users.serializers import ProfileSerializer

from .. import choices, models, selectors, services

logger = logging.getLogger(__name__)


class ModerationStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[c.name for c in choices.ModerationStatus])


class ModerationActionSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=[c.name for c in choices.ModerationStatus])
    created_by = ProfileSerializer()

    class Meta:
        model = models.ModerationAction
        fields = [
            "status",
            "created_at",
            "created_by",
        ]


class CompanyModerateView(ErrorsMixin, generics.GenericAPIView):
    queryset = selectors.get_companies(prefetch=False)
    lookup_field = "slug"
    expected_exceptions = {}
    permission_classes = [IsEditorPermission | IsReadOnly]
    serializer_class = None

    def get(self, request, slug):
        company = self.get_object()
        actions = selectors.get_company_moderation_actions(company)
        serializer = ModerationActionSerializer(actions, many=True)
        return Response(serializer.data)

    def post(self, request, slug):
        """Moderates View"""

        serializer = ModerationStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        status = serializer.validated_data["status"]
        company = self.get_object()
        profile = request.user.profile

        company = services.moderate_company(
            company=company, profile=profile, status=status
        )

        data = {"status": company.status}
        serializer = validate_or_raise(ModerationStatusSerializer, data)
        return Response(serializer.data)


class CompanyRevisionModerateView(ErrorsMixin, generics.GenericAPIView):
    queryset = selectors.get_revisions()
    lookup_field = "id"
    expected_exceptions = {}
    permission_classes = [IsEditorPermission | IsReadOnly]
    serializer_class = None

    def get(self, request, id):
        revision = self.get_object()
        actions = selectors.get_revision_moderation_actions(revision)
        serializer = ModerationActionSerializer(actions, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        """Moderates View"""

        serializer = ModerationStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        status = serializer.validated_data["status"]
        revision = self.get_object()
        profile = request.user.profile

        revision = services.moderate_revision(
            revision=revision, profile=profile, status=status
        )

        data = {"status": revision.status}
        serializer = validate_or_raise(ModerationStatusSerializer, data)
        return Response(serializer.data)
