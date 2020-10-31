from rest_framework import (
    mixins,
    generics,
    serializers,
    pagination,
    permissions,
)
from rest_framework import exceptions as drf_exceptions
from rest_framework.response import Response

from api.common.exceptions import ErrorsMixin
from api.users.serializers import ProfileSerializer
from .. import models, selectors, services


class RequestCommentSerializer(serializers.ModelSerializer):
    thread_id = serializers.IntegerField(required=True)
    parent_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = models.Comment
        fields = ["text", "thread_id", "parent_id"]


class ResponseCommentSerializer(serializers.ModelSerializer):
    clap_count = serializers.IntegerField()
    reply_count = serializers.IntegerField()

    profile = ProfileSerializer()

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
            # TODO Implement recent comments
            # "parent_id",
            # "thread_id",
        ]


class CommentListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ResponseCommentSerializer
    pagination_class = pagination.LimitOffsetPagination
    expected_exceptions = {
        models.Thread.DoesNotExist: drf_exceptions.ValidationError,
        models.Comment.DoesNotExist: drf_exceptions.ValidationError,
    }
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        thread_id = self.request.query_params.get("thread_id", None)
        parent_id = self.request.query_params.get("parent_id", None)
        if parent_id:
            return selectors.get_comment_children(parent_id=parent_id)
        else:
            return selectors.get_thread_comments(thread_id=thread_id)

    def get(self, request):
        return super().list(request)

    def post(self, request):
        serializer = RequestCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data.pop("text")

        parent_id = serializer.validated_data.pop("parent_id", None)
        thread_id = serializer.validated_data.pop("thread_id", None)

        thread = models.Thread.objects.get(id=thread_id)
        parent = None if not parent_id else models.Comment.objects.get(id=parent_id)

        comment = services.create_comment(
            profile=request.user.profile, text=text, thread=thread, parent=parent
        )
        return Response(ResponseCommentSerializer(comment).data)


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
