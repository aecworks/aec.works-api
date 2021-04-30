import logging

from rest_framework import generics, mixins, serializers
from rest_framework.response import Response

from api.common.exceptions import ErrorsMixin
from api.permissions import IsEditorPermission, IsReadOnly
from api.users.serializers import ProfileSerializer

from .. import models, selectors, services

logger = logging.getLogger(__name__)


class CompanyRevisionSerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="slug"
    )
    approved_by = ProfileSerializer(read_only=True)
    created_by = ProfileSerializer(read_only=True)
    cover_url = serializers.SerializerMethodField()
    logo_url = serializers.SerializerMethodField()

    def get_cover_url(self, obj):
        try:
            return obj.cover.file.crop["800x400"].url if obj.cover else None
        except KeyError:
            logger.error(f"failed to cover image for: {obj}")

    def get_logo_url(self, obj):
        try:
            return obj.logo.file.crop["80x80"].url if obj.logo else None
        except KeyError:
            logger.error(f"failed to logo image for: {obj}")

    class Meta:
        model = models.CompanyRevision
        fields = [
            "id",
            "approved_by",
            "created_by",
            "created_at",
            "logo_url",
            "cover_url",
            # *services.updatable_attributes,
            "name",
            "description",
            "website",
            "location",
            "twitter",
            "crunchbase_id",
            "logo",
            "cover",
            "hashtags",
        ]


# class RequestCompanyRevisionSerializer(CompanyRevisionSerializer):
#     class Meta:
#         model = models.CompanyRevision
#         _excluded = ["created_by", "approved_by"]
#         fields = [
#             f
#             for f in CompanyRevisionSerializer.Meta.fields
#             if f not in ["created_by", "approved_by"]
#         ]


class CompanyRevisionListView(
    ErrorsMixin, mixins.RetrieveModelMixin, generics.GenericAPIView
):
    serializer_class = None
    queryset = selectors.get_companies()
    lookup_field = "slug"
    permission_classes = [IsEditorPermission | IsReadOnly]
    expected_exceptions = {}

    def get(self, request, slug):
        company = self.get_object()
        return Response(
            CompanyRevisionSerializer(
                company.revisions.all().order_by("-created_at"), many=True
            ).data
        )

    def post(self, request, slug):
        """ Creates New Company Revision """
        serializer = CompanyRevisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = self.get_object()
        revision = services.create_revision(
            company=company,
            profile=request.user.profile,
            validated_data=serializer.validated_data,
        )
        return Response(CompanyRevisionSerializer(revision).data)


class CompanyRevisionDetailView(ErrorsMixin, generics.GenericAPIView):
    serializer_class = None
    queryset = selectors.get_revisions()
    expected_exceptions = {}
    lookup_field = "id"
    permission_classes = [IsEditorPermission | IsReadOnly]

    def post(self, request, id, action):
        if action == "approve":  # approve
            revision = self.get_object()
            services.apply_revision(revision=revision, profile=request.user.profile)
            return Response(CompanyRevisionSerializer(revision).data)
        else:
            return Response(status=404)
