from io import BytesIO

from PIL import Image as PillowImage

from django.core.files.uploadedfile import SimpleUploadedFile


def generate_image_file(name="test.png", ext="png", size=(50, 50), color=(256, 0, 0)):
    """
    WARNING: Using this with ImageField,
    actually creates image file under MEDIA_ROOT directory
    """
    stream = BytesIO()
    image = PillowImage.new("RGB", size=size, color=color)
    image.save(stream, ext)
    stream.seek(0)
    return SimpleUploadedFile(name, stream.getvalue())
