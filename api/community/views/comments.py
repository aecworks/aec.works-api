from rest_framework import mixins, generics, serializers, pagination
from rest_framework import exceptions as drf_exceptions

from api.common.utils import inline_serializer
from api.common.exceptions import ErrorsMixin
from .. import models, selectors


class OutCommentSerializer(serializers.ModelSerializer):
    clap_count = serializers.IntegerField()
    replies_count = serializers.IntegerField()

    profile = inline_serializer(
        fields={"name": serializers.CharField(), "id": serializers.IntegerField()}
    )

    class Meta:
        model = models.Comment
        fields = [
            #
            "id",
            "created_at",
            "replies_count",
            "clap_count",
            "profile",
            "level",
            "text",
        ]
        # exclude = ["clappers"]


class CommentListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = OutCommentSerializer
    expected_exceptions = {}
    pagination_class = pagination.LimitOffsetPagination
    page_size = 10

    def get_queryset(self):
        thread_id = self.request.query_params.get("thread_id", None)
        parent_id = self.request.query_params.get("parent_id", None)
        if parent_id and not thread_id:
            return selectors.get_comment_children(parent_id=parent_id)
        elif thread_id and not parent_id:
            return selectors.get_thread_comments(thread_id=thread_id)
        else:
            msg = "must provide thread_id or parent_id but not both"
            raise drf_exceptions.ValidationError(msg)

    def get(self, request):
        return super().list(request)
