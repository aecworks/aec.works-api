import pytest

from api.users.factories import UserFactory
from rest_framework_simplejwt.tokens import AccessToken

# from django.core.files.uploadedfile import SimpleUploadedFile
# from api.community import factories as f


@pytest.fixture
def jwt_auth_header(client, django_user_model):
    user = UserFactory()
    token = AccessToken.for_user(user)
    return dict(HTTP_AUTHORIZATION="JWT {}".format(token))


def test_image_upload(client, jwt_auth_header):
    url = "/images/upload/filename.png"
    # from django.core.files.uploadedfile import SimpleUploadedFile
    # file = SimpleUploadedFile("test.py")
    # with open("README.md") as fp:
    # from io import BytesIO
    # img = BytesIO(b"mybinarydata")
    # img.name = "myimage.jpg"
    # TODO Properly test this
    resp = client.put(url, data="xxx")
    assert resp.status_code == 201
