from rest_framework.test import APIRequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile

from api.users.factories import UserFactory
from api.images.views import ImageUploadView


def test_image_upload(auth_client):
    # TODO can this be improved?
    url = "/images/upload/filename.png"
    tmp_file = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpg")
    factory = APIRequestFactory()
    request = factory.put(url)
    request.data = dict(file=tmp_file)
    request.user = UserFactory()
    resp = ImageUploadView().put(request, filename="test.png")
    assert resp.status_code == 201
    assert resp.data
