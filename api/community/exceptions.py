from rest_framework import status
from rest_framework.exceptions import APIException


class TooManyPendingReviewsError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "non-editor user exceeded limit of unmoderated reviews"
    default_code = "conflict"


class CompanyNameExistsError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Company with the same name already exists"
    default_code = "conflict"
