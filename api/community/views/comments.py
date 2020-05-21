from rest_framework import mixins, generics, serializers, pagination
from rest_framework import exceptions as drf_exceptions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.common.utils import inline_serializer
from api.common.exceptions import ErrorsMixin
from .. import models, selectors, services


class InCommentSerializer(serializers.ModelSerializer):
    thread_id = serializers.IntegerField(required=True)

    class Meta:
        model = models.Comment
        fields = ["text", "thread_id"]


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


class CommentListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = OutCommentSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    expected_exceptions = {models.Thread.DoesNotExist: drf_exceptions.ValidationError}
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

    def post(self, request):
        serializer = InCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        thread_id = serializer.validated_data["thread_id"]
        text = serializer.validated_data["text"]

        thread = selectors.get_thread(id=thread_id)
        _ = services.create_thread_comment(
            profile=request.user.profile, thread=thread, text=text
        )
        return Response(serializer.data)
        # TODO
        # Can't use Serializer becase of annotations in selectors
        # Maybe annotation and prefetch need to move into a manager?
        # response_serializer = OutCommentSerializer(comment)
        # return Response(response_serializer.data)
