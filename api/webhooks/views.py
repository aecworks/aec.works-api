from rest_framework import generics, serializers, permissions
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from api.common.exceptions import ErrorsMixin
from api.community.selectors import get_company_from_twitter_handle
from api.community.services import create_company_article


class WebhookSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)
    text = serializers.CharField(required=True)
    mentioned = serializers.CharField(required=False)
    hashtags = serializers.CharField(required=False)


class TwitterWebhookView(ErrorsMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = WebhookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data["url"]
        text = serializer.validated_data["text"]
        mentioned = serializer.validated_data.get("mentioned")
        hashtags = serializer.validated_data.get("hashtags")
        print(text)
        print(hashtags)

        company = get_company_from_twitter_handle(mentioned)
        if not mentioned or not company:
            return Response()

        profile = request.user.profile
        create_company_article(company=company, url=url, profile=profile)
        return Response()
