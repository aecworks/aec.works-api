from typing import Tuple
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import requests

User = get_user_model()


class ProviderException(Exception):
    ...


class GithubProvider:

    API_URL = "https://api.github.com"
    PROFILE_URL = f"{API_URL}/user"
    EMAIL_URL = f"{API_URL}/user/emails"
    DEFAULT_HEADERS = {"Accept": "application/vnd.github.v3+json"}

    @classmethod
    def get_user_data(cls, code) -> Tuple[str, dict]:
        access_token = cls._get_access_token(code)
        email, extra_data = cls._get_user_from_token(access_token)
        return email, extra_data
        # token, _ = Token.objects.get_or_create(user=user)
        # return token

    @classmethod
    def _get_access_token(cls, code):
        payload = dict(
            client_id=settings.GITHUB_CLIENT_ID,
            client_secret=settings.GITHUB_CLIENT_SECRET,
            code=code,
        )
        resp = requests.post(
            "https://github.com/login/oauth/access_token",
            json=payload,
            headers={"Accept": "application/json"},
        )
        response = resp.json()
        try:
            return response["access_token"]
        except KeyError:
            raise ProviderException("Unexpected Response From Github")

    @classmethod
    def _get_user_from_token(cls, access_token):
        headers = {**cls.DEFAULT_HEADERS, "Authorization": f"token {access_token}"}
        email_data = requests.get(cls.EMAIL_URL, headers=headers).json()
        for i in email_data:
            if i["primary"]:
                email = i["email"]
                break
        else:
            raise ProviderException("could not get user email")

        user_data = requests.get(cls.PROFILE_URL, headers=headers).json()
        profile_data = dict(
            # model field = payload key
            github_url=user_data.get("html_url", None),
            bio=user_data.get("bio", None),
            avatar_url=user_data.get("avatar_url", None),
            location=user_data.get("location", None),
        )

        return email, profile_data
