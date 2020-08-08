from rest_framework import (
    mixins,
    generics,
    serializers,
    pagination,
    permissions,
    decorators,
)
from rest_framework import exceptions as drf_exceptions
from rest_framework.response import Response

from api.common.utils import inline_serializer
from api.common.exceptions import ErrorsMixin
from .. import models, selectors, services


class RequestCommentSerializer(serializers.ModelSerializer):
    thread_id = serializers.IntegerField(required=True)

    class Meta:
        model = models.Comment
        fields = ["text", "thread_id"]


class ResponseCommentSerializer(serializers.ModelSerializer):
    clap_count = serializers.IntegerField()
    reply_count = serializers.IntegerField()

    profile = inline_serializer(
        fields={"name": serializers.CharField(), "slug": serializers.CharField()}
    )

    class Meta:
        model = models.Comment
        fields = [
            #
            "id",
            "created_at",
            "reply_count",
            "clap_count",
            "profile",
            "level",
            "text",
        ]


class CommentListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ResponseCommentSerializer
    pagination_class = pagination.LimitOffsetPagination
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

    @decorators.permission_classes([permissions.IsAuthenticatedOrReadOnly])
    def get(self, request):
        return super().list(request)

    @decorators.permission_classes([permissions.IsAuthenticatedOrReadOnly])
    def post(self, request):
        serializer = RequestCommentSerializer(data=request.data)
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
        # response_serializer = ResponseCommentSerializer(comment)
        # return Response(response_serializer.data)


class CommentClapView(ErrorsMixin, generics.GenericAPIView):
    serializer_class = ResponseCommentSerializer
    queryset = selectors.get_comments()
    expected_exceptions = {}
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        comment = self.get_object()
        profile = request.user.profile
        result = services.comment_clap(comment=comment, profile=profile)
        return Response(result)
