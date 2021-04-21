from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.http import condition
from rest_framework import filters, generics, mixins, permissions, serializers

from api.common.exceptions import ErrorsMixin

from .. import annotations, caching, selectors


class HashtagDetailSerializer(serializers.Serializer):
    ...
    # links to posts/companies


class HashtagListSerializer(serializers.Serializer):
    slug = serializers.CharField()
    company_count = serializers.CharField()


class HashtagListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = HashtagListSerializer
    queryset = selectors.get_hashtags()
    pagination_class = None
    expected_exceptions = {}
    permission_classes = [permissions.AllowAny]

    search_fields = ["slug"]
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        return annotations.annotate_company_count(selectors.get_hashtags())

    @method_decorator(cache_control(max_age=60))
    @method_decorator(condition(last_modified_func=caching.hashtag_last_modified))
    def get(self, request):
        return super().list(request)
