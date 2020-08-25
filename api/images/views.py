from rest_framework import views, serializers
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from .service import create_image


class ImageResponseSerializer(serializers.Serializer):
    url = serializers.ImageField(source="image")


class ImageRequestSerializer(serializers.Serializer):
    image = serializers.ImageField()


class ImageUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        file = request.data["file"]
        temp_image = create_image(image_file=file)
        return Response(ImageResponseSerializer(temp_image).data, status=201)
