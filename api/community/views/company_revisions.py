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
            "id",
            "created_by",
            "created_at",
            "logo_url",
            "cover_url",
        ]


class ResponseDetailCompanyRevisionSerializer(ResponseCompanyRevisionSerializer):
    created_by = ProfileSerializer(read_only=True)

    class Meta:
        model = models.CompanyRevision
        fields = RequestCompanyRevisionSerializer.Meta.fields + [
            "approved_by",
            "created_by",
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

        hashtag_names = serializer.validated_data.pop("hashtags", [])
        hashtags = services.get_or_create_hashtags(hashtag_names)

        attrs = services.CompanyRevisionAttributes(
            **serializer.validated_data, hashtags=hashtags
        )
        revision = services.create_revision(
            company=company, created_by=profile, attrs=attrs
        )
        return Response(ResponseCompanyRevisionSerializer(revision).data)
