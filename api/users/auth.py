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
        email, user_data, profile_data = cls._get_user_from_token(access_token)
        return email, user_data, profile_data

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
        gh_email_data = requests.get(cls.EMAIL_URL, headers=headers).json()
        for i in gh_email_data:
            if i["primary"]:
                email = i["email"]
                break
        else:
            raise ProviderException("could not get user email")

        gh_user_data = requests.get(cls.PROFILE_URL, headers=headers).json()

        # avatar_url = gh_user_data.get("avatar_url", None)
        user_data = dict(name=gh_user_data["name"])
        profile_data = dict(
            # model field = payload key
            github_url=gh_user_data.get("html_url", None),
            bio=gh_user_data.get("bio", None),
            location=gh_user_data.get("location", None),
        )

        return email, user_data, profile_data
