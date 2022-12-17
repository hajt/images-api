import pytest

from ..models import Image
from .factories import ImageFactory
from .helpers import generate_image_file


@pytest.mark.django_db
def test_image_repr():
    image = ImageFactory(file=generate_image_file())
    assert image.__repr__() == f"<{Image.__name__}({image.title})>"


@pytest.mark.django_db
def test_image_str():
    image = ImageFactory(file=generate_image_file())
    assert image.__str__() == image.title


@pytest.mark.django_db
def test_image_dimensions_fields():
    image = ImageFactory(file=generate_image_file())
    assert image.width == image.file.width
    assert image.height == image.file.height


@pytest.mark.django_db
def test_image_resize():
    image = ImageFactory(file=generate_image_file())
    image.width = 100
    image.height = 100
    image.save()
    assert image.file.height == 100
    assert image.file.width == 100


@pytest.mark.django_db
def test_image_resize_only_one_new_dimension():
    image = ImageFactory(file=generate_image_file())

    image.width = 100
    image.save()
    assert image.file.width == 100

    image.height = 100
    image.save()
    assert image.file.height == 100
