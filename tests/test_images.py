import pytest


def test_image_upload(auth_client):
    url = "/images/upload/filename.png"
    # from django.core.files.uploadedfile import SimpleUploadedFile
    # file = SimpleUploadedFile("test.py")
    # with open("README.md") as fp:
    # from io import BytesIO
    # img = BytesIO(b"mybinarydata")
    # img.name = "myimage.jpg"
    # TODO Properly test this
    resp = auth_client.put(url, data="xxx")
    assert resp.status_code == 201
