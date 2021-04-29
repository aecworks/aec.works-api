from rest_framework import status
from rest_framework.exceptions import APIException


class TooManyPendingReviews(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "User Has Too Many Pending Reviews"
    default_code = "conflict"
