from urllib.parse import unquote, urlencode, urlparse
from rest_framework import mixins, generics, serializers, views
from rest_framework.response import Response
from rest_framework import exceptions as drf_exceptions
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import redirect
from djoser.utils import login_user

from api.common.exceptions import ErrorsMixin
from . import selectors
from .services import get_jwt_for_user, get_token_for_user
from .auth import GithubProvider, ProviderException
from .models import Profile
from .choices import UserSourceChoices


class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.SerializerMethodField()
    name = serializers.CharField()

    def get_email(self, obj):
        return obj.user.email

    class Meta:
        model = Profile
        exclude = ["user"]


class ProfileListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    pagination_class = LimitOffsetPagination
    page_size = 100

    def get(self, request):
        return super().list(request)


class ProfileDetailView(
    ErrorsMixin, mixins.RetrieveModelMixin, generics.GenericAPIView
):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get(self, request, pk):
        return super().retrieve(request, pk)


class GithubView(ErrorsMixin, views.APIView):
    expected_exceptions = {ProviderException: drf_exceptions.ValidationError}
    queryset = 1

    def post(self, request):
        code = request.query_params.get("code")
        if not code:
            raise drf_exceptions.ValidationError("code is missing")

        # TODO - move to service
        email, profile_data = GithubProvider.get_user_data(code)
        user = selectors.get_or_create_user(
            email=email, defaults={"source": UserSourceChoices.GITHUB.name}
        )
        for key, value in profile_data.items():
            setattr(user.profile, key, value)
            # TODO. set avatar from avatar_url
        user.profile.save()
        jwt_dict = get_jwt_for_user(user)
        return Response(jwt_dict)
