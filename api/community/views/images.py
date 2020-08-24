from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from api.community.services import create_temp_image


class ImageUploadView(APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        file = request.data["file"]
        image = create_temp_image(image=file)
        breakpoint()
        return Response(status=200)
        #     # For multipart parser only
        #     # parser_classes = [MultiPartParser]
        #     # accepts json
