from rest_framework import mixins, generics, serializers, permissions

# from rest_framework import exceptions as drf_exceptions
# from rest_framework.pagination import LimitOffsetPagination
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
    # pagination_class = LimitOffsetPagination
    # page_size = 50
    expected_exceptions = {}
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return super().list(request)
