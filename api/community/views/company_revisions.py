import logging

from rest_framework import generics, mixins, serializers
from rest_framework.response import Response

from api.common.exceptions import ErrorsMixin
from api.permissions import IsEditorPermission, IsReadOnly
from api.users.serializers import ProfileSerializer

from .. import models, selectors, services

logger = logging.getLogger(__name__)


class RequestCompanyRevisionSerializer(serializers.ModelSerializer):
    hashtags = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = models.CompanyRevision
        fields = [
            # CompanyAttributes
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


class ResponseCompanyRevisionSerializer(RequestCompanyRevisionSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="slug"
    )
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
        fields = RequestCompanyRevisionSerializer.Meta.fields + [
            # TODO remove cover, logo ints
            "id",
            "created_by",
            "created_at",
            "logo_url",
            "cover_url",
        ]


class ResponseDetailCompanyRevisionSerializer(ResponseCompanyRevisionSerializer):
    created_by = ProfileSerializer(read_only=True)
    status = serializers.CharField()

    class Meta:
        model = models.CompanyRevision
        fields = ResponseCompanyRevisionSerializer.Meta.fields + [
            "created_by",
            "status",
        ]


class ResponseRevisionHistory(serializers.ModelSerializer):
    created_by = ProfileSerializer(read_only=True)
    revision = ResponseDetailCompanyRevisionSerializer()

    class Meta:
        model = models.CompanyRevisionHistory
        fields = [
            "created_at",
            "created_by",
            "revision",
        ]


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
            ResponseCompanyRevisionSerializer(
                company.revisions.all().order_by("-created_at"), many=True
            ).data
        )

    def post(self, request, slug):
        """ Creates New Company Revision """
        serializer = RequestCompanyRevisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = request.user.profile
        company = self.get_object()

        revision = services.create_revision(
            company=company, created_by=profile, **serializer.validated_data,
        )
        return Response(ResponseCompanyRevisionSerializer(revision).data)


class CompanyRevisionApplyView(ErrorsMixin, generics.GenericAPIView):
    queryset = selectors.get_revisions()
    lookup_field = "id"
    expected_exceptions = {}
    permission_classes = [IsEditorPermission | IsReadOnly]
    serializer_class = None

    def post(self, request, id):
        """ Sets Revision """

        revision = self.get_object()
        profile = request.user.profile

        history = services.apply_revision(profile=profile, revision=revision)

        return Response(ResponseRevisionHistory(history).data)
