from rest_framework import filters, generics, mixins, permissions, serializers

from api.common.exceptions import ErrorsMixin

from .. import selectors


class HashtagDetailSerializer(serializers.Serializer):
    ...
    # links to posts/companies


class HashtagListSerializer(serializers.Serializer):
    slug = serializers.CharField()
    company_count = serializers.CharField()
    post_count = serializers.CharField()


class HashtagListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = HashtagListSerializer
    queryset = selectors.get_hashtags()
    pagination_class = None
    expected_exceptions = {}
    permission_classes = [permissions.AllowAny]

    search_fields = ["slug"]
    filter_backends = [filters.SearchFilter]

    def get(self, request):
        return super().list(request)
