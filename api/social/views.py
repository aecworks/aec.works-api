from rest_framework.response import Response
from rest_framework import views, exceptions
from tweepy.error import TweepError

from api.common.exceptions import ErrorsMixin
from .twitter import get_timeline


class TweetTimelineView(ErrorsMixin, views.APIView):
    permission_classes = []
    expected_exceptions = {TweepError: exceptions.APIException}

    def get(self, request, handle):
        tweets = get_timeline(handle, num=5)
        return Response(tweets)
