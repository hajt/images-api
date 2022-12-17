import pytest

from django.conf import settings

from ..serializers import (
    ImageCreateSerializer,
    ImagePartialUpdateSerializer,
    ImageSerializer,
)
from .factories import ImageFactory
from .helpers import generate_image_file


@pytest.mark.django_db
def test_image_serialization():
    image = ImageFactory(file=generate_image_file())
    serializer = ImageSerializer(image)
    assert serializer.data["id"] == str(image.id)
    assert serializer.data["title"] == image.title
    assert serializer.data["width"] == image.width
    assert serializer.data["height"] == image.height
    assert serializer.data["file"] == settings.MEDIA_URL + str(image.file)


@pytest.mark.django_db
def test_image_create_deserialization():
    data = {"title": "Test", "width": 100, "height": 100, "file": generate_image_file()}
    serializer = ImageCreateSerializer(data=data)
    assert serializer.is_valid()


@pytest.mark.parametrize(
    "data",
    (
        {"title": "Test"},
        {"width": 100},
        {"height": 100},
        {"file": generate_image_file()},
    ),
)
@pytest.mark.django_db
def test_image_partial_update_deserialization(data):
    serializer = ImagePartialUpdateSerializer(data=data)
    assert serializer.is_valid()
