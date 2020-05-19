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

    email = serializers.SerializerMethodField()
    name = serializers.CharField()

    def get_email(self, obj):
        return obj.user.email

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

        email, profile_data = GithubProvider.get_user_data(code)
        user = selectors.get_or_create_user(
            email=email, defaults={"source": UserSourceChoices.GITHUB.name}
        )
        # TODO. set avatar image from avatar_url
        services.set_profile_data(user=user, profile_data=profile_data)
        jwt_dict = services.get_jwt_for_user(user)
        return Response(jwt_dict)
