from .models import Image


def create_image(*, image_file) -> Image:
    return Image.objects.create(image=image_file)
