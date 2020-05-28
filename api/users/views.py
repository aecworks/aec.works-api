from rest_framework import mixins, generics, serializers, views
from rest_framework.response import Response
from rest_framework import exceptions as drf_exceptions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from api.common.exceptions import ErrorsMixin
from . import selectors, services
from .auth import GithubProvider, ProviderException
from .models import Profile
from .choices import UserSourceChoices


class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        model = Profile
        exclude = ["user", "id"]


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
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get(self, request, pk):
        return super().retrieve(request, pk)


class ProfileMeView(ErrorsMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user.profile)
        return Response(serializer.data)


class GithubView(ErrorsMixin, views.APIView):
    expected_exceptions = {ProviderException: drf_exceptions.ValidationError}
    queryset = 1

    def post(self, request):
        code = request.query_params.get("code")
        if not code:
            raise drf_exceptions.ValidationError("code is missing")

        email, user_data, profile_data = GithubProvider.get_user_data_from_code(code)
        user_data.update({"source": UserSourceChoices.GITHUB.name})

        user = services.create_or_update_user(email=email, defaults=user_data)
        services.update_profile(user=user, defaults=profile_data)
        # TODO. set avatar image from avatar_url

        jwt_dict = services.get_jwt_for_user(user)
        return Response(jwt_dict)
