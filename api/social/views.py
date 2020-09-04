from rest_framework.response import Response
from rest_framework import (
    views,
    # serializers,
    # permissions,
)

from api.common.exceptions import ErrorsMixin
from .twitter import get_timeline


class TweetTimelineView(ErrorsMixin, views.APIView):
    permission_classes = []

    def get(self, request, handle):
        tweets = get_timeline(handle)
        return Response({"tweeets": tweets})
