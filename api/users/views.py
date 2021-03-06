from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import exceptions as drf_exceptions
from rest_framework import filters, generics, mixins, views
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.common.exceptions import ErrorsMixin

from . import selectors, services
from .auth import GithubProvider, LinkedInProvider, ProviderException
from .choices import UserProviderChoices
from .models import Profile
from .serializers import LoginSerializer, ProfileDetailSerializer, ProfileSerializer


class ProfileListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ProfileSerializer
    queryset = selectors.get_profiles()
    pagination_class = LimitOffsetPagination
    page_size = 100

    search_fields = ["bio", "location", "user__name"]
    filter_backends = [filters.SearchFilter]

    @method_decorator(cache_page(60))
    def get(self, request):
        return super().list(request)


class ProfileDetailView(
    ErrorsMixin, mixins.RetrieveModelMixin, generics.GenericAPIView
):
    serializer_class = ProfileDetailSerializer
    queryset = Profile.objects.all()
    lookup_field = "slug"

    @method_decorator(cache_page(60))
    def get(self, request, slug):
        return super().retrieve(request, slug)


class ProfileMeView(ErrorsMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileDetailSerializer
    queryset = selectors.get_profiles()

    def get(self, request):
        user = request.user
        profile = selectors.get_profiles().get(user=user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class OauthLoginView(ErrorsMixin, views.APIView):
    expected_exceptions = {ProviderException: drf_exceptions.ValidationError}

    def post(self, request, provider_name):
        code = request.query_params.get("code")
        redirect_uri = request.query_params.get("redirect_uri")
        if not code:
            raise drf_exceptions.ValidationError("code is missing")

        providers = {
            UserProviderChoices.LINKEDIN.value: LinkedInProvider,
            UserProviderChoices.GITHUB.value: GithubProvider,
        }
        if provider_name not in providers:
            raise drf_exceptions.NotFound(f"provider not supported: {provider_name}")

        provider = providers[provider_name]

        email, user_data, profile_data = provider.get_user_data_from_code(
            code, redirect_uri
        )
        user = services.create_or_update_user(email=email, user_data=user_data)
        services.update_profile(user=user, profile_data=profile_data)

        login(request, user)
        return Response(status=200)


class Logout(ErrorsMixin, views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=200)


class Login(ErrorsMixin, views.APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response(ProfileDetailSerializer(user.profile).data, status=200)
        raise drf_exceptions.AuthenticationFailed()
