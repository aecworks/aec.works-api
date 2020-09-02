from unittest import mock
from rest_framework.test import APIRequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile

from api.users.factories import UserFactory
from api.images.views import ImageUploadView


@mock.patch("api.images.views.create_image")
def test_image_upload(m_create_image, auth_client):
    # TODO can this be improved?
    url = "/images/upload/filename.png"
    tmp_file = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpg")
    factory = APIRequestFactory()
    request = factory.put(url)
    request.data = dict(file=tmp_file)
    request.user = UserFactory()
    resp = ImageUploadView().put(request, filename="test.png")

    assert m_create_image.called
    assert resp.status_code == 201
    assert resp.data
