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
    thread_id = serializers.IntegerField(required=False)
    parent_id = serializers.IntegerField(required=False)

    def validate(self, data):
        if "thread_id" not in data and "parent_id" not in data:
            raise serializers.ValidationError("thread_id or parent_id required")
        elif "thread_id" in data and "parent_id" in data:
            raise serializers.ValidationError(
                "thread_id or parent_id required but not both"
            )
        return data

    class Meta:
        model = models.Comment
        fields = ["text", "thread_id", "parent_id"]


class ResponseCommentSerializer(serializers.ModelSerializer):
    clap_count = serializers.IntegerField(default=0)
    reply_count = serializers.IntegerField(default=0)

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
        ]


class CommentListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ResponseCommentSerializer
    pagination_class = pagination.LimitOffsetPagination
    expected_exceptions = {
        models.Thread.DoesNotExist: drf_exceptions.ValidationError,
        models.Comment.DoesNotExist: drf_exceptions.ValidationError,
    }
    page_size = 10
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
        serializer = RequestCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data.pop("text")
        parent_id = serializer.validated_data.pop("parent_id", None)
        thread_id = serializer.validated_data.pop("thread_id", None)
        if thread_id:
            thread = models.Thread.objects.get(id=thread_id)
            parent_kwarg = dict(thread=thread)
        else:
            comment = models.Comment.objects.get(id=parent_id)
            parent_kwarg = dict(parent=comment)
        comment = services.create_comment(
            profile=request.user.profile, text=text, **parent_kwarg
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
