from rest_framework import views, serializers, permissions
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from .service import create_image


class ImageResponseSerializer(serializers.Serializer):
    url = serializers.ImageField(source="image")
    created_at = serializers.DateTimeField()


class ImageRequestSerializer(serializers.Serializer):
    image = serializers.ImageField()


class ImageUploadView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        file = request.data["file"]
        image = create_image(image_file=file, user=request.user)
        return Response(ImageResponseSerializer(image).data, status=201)
