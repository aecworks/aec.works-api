from rest_framework import mixins, generics, views
from rest_framework.response import Response
from rest_framework import exceptions as drf_exceptions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from api.common.exceptions import ErrorsMixin
from . import selectors, services
from .auth import GithubProvider, LinkedInProvider, ProviderException
from .models import Profile
from .choices import UserProviderChoices

from .serializers import ProfileSerializer, ProfileDetailSerializer


class ProfileListView(ErrorsMixin, mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ProfileSerializer
    queryset = selectors.get_profiles()
    pagination_class = LimitOffsetPagination
    page_size = 100

    def get(self, request):
        return super().list(request)


class ProfileDetailView(
    ErrorsMixin, mixins.RetrieveModelMixin, generics.GenericAPIView
):
    serializer_class = ProfileDetailSerializer
    queryset = Profile.objects.all()
    lookup_field = "slug"

    def get(self, request, slug):
        return super().retrieve(request, slug)


class ProfileMeView(ErrorsMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileDetailSerializer
    queryset = Profile.objects.all()

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user.profile)
        return Response(serializer.data)


class OauthLoginView(ErrorsMixin, views.APIView):
    expected_exceptions = {ProviderException: drf_exceptions.ValidationError}

    def post(self, request, provider_name):
        code = request.query_params.get("code")
        if not code:
            raise drf_exceptions.ValidationError("code is missing")

        providers = {
            UserProviderChoices.LINKEDIN.value: LinkedInProvider,
            UserProviderChoices.GITHUB.value: GithubProvider,
        }
        if provider_name not in providers:
            raise drf_exceptions.NotFound(f"provider not supported: {provider_name}")

        provider = providers[provider_name]

        email, user_data, profile_data = provider.get_user_data_from_code(code)
        user_data.update({"source": provider_name})

        user = services.create_or_update_user(email=email, defaults=user_data)
        services.update_profile(user=user, defaults=profile_data)

        jwt_dict = services.get_jwt_for_user(user)
        return Response(jwt_dict)
