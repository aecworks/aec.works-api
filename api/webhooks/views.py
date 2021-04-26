import logging

from rest_framework import exceptions, generics, permissions, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from api.common.exceptions import ErrorsMixin

from .services import (
    TweetCompanyReferenceNotFound,
    create_article_from_tweet,
    is_add_article,
    resolve_company,
)

logger = logging.getLogger(__name__)


class WebhookSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)
    url = serializers.URLField(allow_blank=True, allow_null=True, required=False)
    mentioned = serializers.CharField(required=True, allow_null=True, allow_blank=True)


class TwitterWebhookView(ErrorsMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    expected_exceptions = {TweetCompanyReferenceNotFound: exceptions.ValidationError}

    def post(self, request):
        """
        This endopint is hit by a Zappier automation everytime @aecworks tweets
        Zapier payloads is defined in `WebhookSerializer`
        """
        """
        text: 'https://t.co/kaRztBg4Qn\n\n@MyAbodu \n#aecworks'
        'https://www.latimes.com/entertainment-arts/story/2021-03-05/new-city-program-brings-high-design-concepts-to-granny-flat'
        """
        serializer = WebhookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data["url"]
        text = serializer.validated_data["text"]
        mentioned = serializer.validated_data.get("mentioned")

        if not is_add_article(text):
            msg = "twitter: doesnt match pattern add <url> to <mention>"
            logger.info(msg)
            return Response(msg, status=200)

        if not url:
            msg = "twitter: no expanded url"
            logger.info(msg)
            return Response(msg, status=200)

        company = resolve_company(text, mentioned)

        if not company:
            msg = "twitter: did not match anh company"
            logger.info(msg)
            return Response(msg, status=200)

        profile = request.user.profile
        article = create_article_from_tweet(company=company, url=url, profile=profile)
        logger.info(f"article '{url}' to '{company.slug}' by '{profile}'")

        return Response(article.id, status=201)
