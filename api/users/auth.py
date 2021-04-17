from typing import Tuple, NamedTuple
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
import requests

from .choices import UserProviderChoices

logger = logging.getLogger(__name__)
User = get_user_model()


class ProviderException(Exception):
    ...


class UserData(NamedTuple):
    name: str
    provider: str


class ProfileData(NamedTuple):
    avatar_url: str = ""
    github: str = ""
    bio: str = ""
    location: str = ""
    twitter: str = ""


class BaseProvider:
    NAME: str
    API_URL: str
    PROFILE_URL: str
    EMAIL_URL: str
    DEFAULT_HEADERS: dict
    AUTH_URL: str
    AUTH_HEADER: dict
    AUTH_PARAMS: dict

    @classmethod
    def get_user_data_from_code(
        cls, code, redirect_uri
    ) -> Tuple[str, UserData, ProfileData]:
        access_token = cls._get_access_token(code, redirect_uri)
        email, user_data, profile_data = cls._agg_user_data(access_token)
        return email, user_data, profile_data

    @classmethod
    def _get_access_token(cls, code, redirect_uri):
        params = {"code": code, "redirect_uri": redirect_uri, **cls.AUTH_PARAMS}
        resp = requests.post(cls.AUTH_URL, params=params, headers=cls.AUTH_HEADER,)
        if resp.status_code != 200:
            raise ProviderException(f"{cls.NAME}: {resp.status_code} {resp.content}")

        try:
            response = resp.json()
            return response["access_token"]
        except KeyError:
            logger.error(f"provider error: {cls.NAME}: {resp.content}")
            raise ProviderException(f"unexpected response from {cls.NAME}")

    @classmethod
    def _agg_user_data(cls, access_token) -> Tuple[str, UserData, ProfileData]:
        raise NotImplementedError("provider must define user data aggregation method")


class GithubProvider(BaseProvider):

    NAME = UserProviderChoices.GITHUB.name
    API_URL = "https://api.github.com"
    PROFILE_URL = f"{API_URL}/user"
    EMAIL_URL = f"{API_URL}/user/emails"
    DEFAULT_HEADERS = {"Accept": "application/vnd.github.v3+json"}
    AUTH_URL = "https://github.com/login/oauth/access_token"
    AUTH_HEADER = {"Accept": "application/json"}
    AUTH_PARAMS = {
        "client_id": settings.OAUTH_GITHUB_CLIENT_ID,
        "client_secret": settings.OAUTH_GITHUB_CLIENT_SECRET,
    }

    @classmethod
    def _agg_user_data(cls, access_token) -> Tuple[str, UserData, ProfileData]:
        """
        Payload https://developer.github.com/v3/users/#get-a-user
        """
        headers = {**cls.DEFAULT_HEADERS, "Authorization": f"token {access_token}"}
        gh_email_data = requests.get(cls.EMAIL_URL, headers=headers).json()
        for i in gh_email_data:
            if i["primary"]:
                email = i["email"]
                break
        else:
            raise ProviderException("could not get user email")

        gh_user_data = requests.get(cls.PROFILE_URL, headers=headers).json()

        profile_photo_url = gh_user_data.get("avatar_url", None)

        # 'name' can be null, fallback to username
        name = gh_user_data["name"] or gh_user_data["login"]
        user_data = UserData(name=name, provider=GithubProvider.NAME)
        profile_data = ProfileData(
            avatar_url=profile_photo_url,
            github=gh_user_data["login"],
            bio=gh_user_data.get("bio", None),
            location=gh_user_data.get("location", None),
            twitter=gh_user_data.get("twitter_username", None),
        )

        return email, user_data, profile_data


class LinkedInProvider(BaseProvider):

    NAME = UserProviderChoices.LINKEDIN.name
    API_URL = "https://api.linkedin.com"
    PROFILE_URL = f"{API_URL}/v2/me"
    EMAIL_URL = f"{API_URL}/v2/clientAwareMemberHandles?q=members&projection=(elements*(handle~))"
    AVATAR_URL = f"{API_URL}/v2/me?projection=(id,profilePicture(displayImage~digitalmediaAsset:playableStreams))"

    AUTH_URL = "https://www.linkedin.com/oauth/v2/accessToken"
    AUTH_HEADER = {"Accept": "x-www-form-urlencoded"}
    AUTH_PARAMS = {
        "client_id": settings.OAUTH_LINKEDIN_CLIENT_ID,
        "client_secret": settings.OAUTH_LINKEDIN_CLIENT_SECRET,
        "grant_type": "authorization_code",
    }

    @classmethod
    def _agg_user_data(cls, access_token) -> Tuple[str, UserData, ProfileData]:
        """
        profile_data = {
            "id": "1Trcn3NVi9",
            "localizedFirstName": "Gui"
            "localizedLastName": "Talarico",
            "profilePicture": {
                "displayImage": "urn:li:digitalmediaAsset:C4E03AQGbbIgo-soGlg"
            },
            "firstName": {
                "localized": {
                    "en_US": "Gui"
                },
                "preferredLocale": {
                    "country": "US",
                    "language": "en"
                }
            },
            "lastName": {
                "localized": {
                    "en_US": "Talarico"
                },
                "preferredLocale": {
                    "country": "US",
                    "language": "en"
                }
            },
        }
        email = {
            "elements": [
                {
                    "handle": "urn:li:emailAddress:471527981",
                    "handle~": {
                        "emailAddress": "gtalarico@gmail.com"
                    }
                }
            ]
        }
        photo_data = {
            "profilePicture": {
                "displayImage": "urn:li:digitalmediaAsset:C4E03AQGbbIgo-soGlg",
                "displayImage~": {
                    "paging": {
                        "count": 10,
                        "start": 0,
                        "links": []
                    },
                    "elements": [
                        ... 100, 200, 400
                        {
                            "artifact": "urn:li:digitalmediaMediaArtifact:(urn:li:digitalmediaAsset:C4E03AQGbbIgo-soGlg,urn:li:digitalmediaMediaArtifactClass:profile-displayphoto-shrink_800_800)",
                            "authorizationMethod": "PUBLIC",
                            "data": {
                                "com.linkedin.digitalmedia.mediaartifact.StillImage": {
                                    "mediaType": "image/jpeg",
                                    "rawCodecSpec": {
                                        "name": "jpeg",
                                        "type": "image"
                                    },
                                    "displaySize": {
                                        "width": 800.0,
                                        "uom": "PX",
                                        "height": 800.0
                                    },
                                    "storageSize": {
                                        "width": 800,
                                        "height": 800
                                    },
                                    "storageAspectRatio": {
                                        "widthAspect": 1.0,
                                        "heightAspect": 1.0,
                                        "formatted": "1.00:1.00"
                                    },
                                    "displayAspectRatio": {
                                        "widthAspect": 1.0,
                                        "heightAspect": 1.0,
                                        "formatted": "1.00:1.00"
                                    }
                                }
                            },
                            "identifiers": [
                                {
                                    "identifier": "https://media-exp1.licdn.com/dms/image/C4E03AQGbbIgo-soGlg/profile-displayphoto-shrink_800_800/0?e=1603929600&v=beta&t=wzS2UQ-_u5cS5cM1xZJNVB3HneHqSHCwDoFlN5eu_80",
                                    "index": 0,
                                    "mediaType": "image/jpeg",
                                    "file": "urn:li:digitalmediaFile:(urn:li:digitalmediaAsset:C4E03AQGbbIgo-soGlg,urn:li:digitalmediaMediaArtifactClass:profile-displayphoto-shrink_800_800,0)",
                                    "identifierType": "EXTERNAL_URL",
                                    "identifierExpiresInSeconds": 1603929600
                                }
                            ]
                        }
                    ]
                }
            },
            "id": "1Trcn3NVi9"
        }
        """
        headers = {"Authorization": f"Bearer {access_token}"}

        profile_data = requests.get(cls.PROFILE_URL, headers=headers).json()
        email_data = requests.get(cls.EMAIL_URL, headers=headers).json()

        email = email_data["elements"][0]["handle~"]["emailAddress"]

        name = "{localizedFirstName} {localizedLastName}".format(**profile_data)
        user_data = UserData(name=name, provider=LinkedInProvider.NAME)

        photo_data = requests.get(cls.AVATAR_URL, headers=headers).json()
        photo_url = photo_data["profilePicture"]["displayImage~"]["elements"][-1][
            "identifiers"
        ][0]["identifier"]
        profile_data = ProfileData(avatar_url=photo_url)
        return email, user_data, profile_data
