from rest_framework.response import Response
from rest_framework import (
    views,
    exceptions,
    # serializers,
    # permissions,
)

from api.common.exceptions import ErrorsMixin
from .twitter import get_timeline
from tweepy.error import TweepError


class TweetTimelineView(ErrorsMixin, views.APIView):
    permission_classes = []
    expected_exceptions = {TweepError: exceptions.APIException}

    def get(self, request, handle):
        tweets = get_timeline(handle)
        return Response(tweets)
