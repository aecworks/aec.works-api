from rest_framework import mixins, generics, serializers
from rest_framework_recursive.fields import RecursiveField

from api.common.exceptions import ErrorsMixin
from .. import models, selectors


class OutCommentSerializer(serializers.ModelSerializer):
    claps = serializers.IntegerField()
    replies_count = serializers.IntegerField()

    def get_count(self, obj):
        return obj.get_descendant_count()

    class Meta:
        model = models.Comment
        fields = [
            #
            "id",
            "replies_count",
            "claps",
            "profile",
            "text",
            "created_at",
        ]
        # exclude = ["clappers"]


class CommentListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = OutCommentSerializer
    queryset = selectors.get_root_comments()
    expected_exceptions = {}

    def get(self, request):
        return super().list(request)


class CommentDetailView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = OutCommentSerializer
    expected_exceptions = {}

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return selectors.get_comments(pk)

    def get(self, request, pk):
        return super().list(request, pk)
