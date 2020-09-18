from rest_framework import mixins, generics, views, serializers
from rest_framework.response import Response
from api.common.exceptions import ErrorsMixin

from api.community.services import arti


class WebhookSerializer(serializers.Serializer):
    mentioned = serializers.CharField()
    url = serializers.URLField()
    hashtags = serializers.URLField()
    text = serializers.CharField()


class TwitterWebhookView(ErrorsMixin, views.APIView):
    permission_classes = []

    def get(self, request):
        serializer = WebhookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
