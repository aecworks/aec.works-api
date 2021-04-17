from rest_framework import exceptions, permissions, serializers, views
from rest_framework.response import Response

from .services import create_image_asset
from .utils import UuidNamedFileUploadParser


class ImageAssetResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    url = serializers.ImageField(source="file")
    created_at = serializers.DateTimeField()
    width = serializers.IntegerField()
    height = serializers.IntegerField()
    created_at = serializers.DateTimeField()


class ImageAssetUploadView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [UuidNamedFileUploadParser]

    def put(self, request, **kwargs):
        file = request.data["file"]
        try:
            width = int(request.query_params.get("width", 0))
            height = int(request.query_params.get("height", 0))
        except ValueError:
            raise exceptions.ValidationError("width and height must be numbers")
        image = create_image_asset(
            img_file=file, width=width, height=height, profile=request.user.profile
        )
        return Response(ImageAssetResponseSerializer(image).data, status=201)
