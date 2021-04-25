import re

from rest_framework import exceptions, generics, permissions, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from api.common.exceptions import ErrorsMixin

from .services import TweetCompanyReferenceNotFound, create_article_from_tweet


class WebhookSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)
    url = serializers.URLField(allow_blank=True, allow_null=True, required=False)
    mentioned = serializers.CharField(required=True, allow_null=True, allow_blank=True)
    hashtags = serializers.CharField(required=True, allow_null=True, allow_blank=True)


class TwitterWebhookView(ErrorsMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    expected_exceptions = {TweetCompanyReferenceNotFound: exceptions.ValidationError}

    def post(self, request):
        """
        This endopint is hit by a Zappier automation everytime @aecworks tweets
        Zapier payloads is defined in `WebhookSerializer`
        """

        serializer = WebhookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data["url"]
        text = serializer.validated_data["text"]
        mentioned = serializer.validated_data.get("mentioned")
        hashtags = serializer.validated_data.get("hashtags") or ""

        if not url:
            return Response("twitter: no url", status=200)
        if not re.match("add", text, re.IGNORECASE):
            return Response("twitter: must being with add", status=200)

        profile = request.user.profile
        article = create_article_from_tweet(
            url=url, text=text, mentioned=mentioned, hashtags=hashtags, profile=profile
        )
        return Response(article.id, status=201)
