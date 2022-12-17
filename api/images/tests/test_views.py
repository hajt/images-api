import json

import pytest

from django.conf import settings
from django.urls import reverse

from ..models import Image
from .factories import ImageFactory
from .helpers import generate_image_file


@pytest.mark.django_db
def test_image_view_get_list_images(authenticated_api_client):
    user = authenticated_api_client.user
    image = ImageFactory(user=user, file=generate_image_file())

    expected_response = json.dumps(
        [
            {
                "id": str(image.id),
                "title": image.title,
                "width": image.width,
                "height": image.height,
                "file": f"http://testserver{settings.MEDIA_URL}{image.file}",
            }
        ]
    )

    response = authenticated_api_client.get(reverse("images:images-list"))
    response_data = json.dumps(response.data)

    assert response.status_code == 200
    assert response_data == expected_response


@pytest.mark.django_db
def test_image_view_get_list_no_images(authenticated_api_client):
    response = authenticated_api_client.get(reverse("images:images-list"))

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_image_view_get_list_no_image_owner(authenticated_api_client):
    ImageFactory(file=generate_image_file())
    response = authenticated_api_client.get(reverse("images:images-list"))

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_image_view_get_image(authenticated_api_client):
    user = authenticated_api_client.user
    image = ImageFactory(user=user, file=generate_image_file())
    expected_response = {
        "id": str(image.id),
        "title": image.title,
        "width": image.width,
        "height": image.height,
        "file": f"http://testserver{settings.MEDIA_URL}{image.file}",
    }

    response = authenticated_api_client.get(
        reverse("images:images-detail", args=[image.id])
    )

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_image_view_get_image_no_image_owner(authenticated_api_client):
    image = ImageFactory(file=generate_image_file())

    response = authenticated_api_client.get(
        reverse("images:images-detail", args=[image.id])
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_image_view_post_image(authenticated_api_client):
    data = {"title": "Test", "width": 100, "height": 100, "file": generate_image_file()}

    response = authenticated_api_client.post(reverse("images:images-list"), data=data)

    assert response.status_code == 201
    assert response.data["title"] == "Test"
    assert response.data["width"] == 100
    assert response.data["height"] == 100
    assert response.data["file"]


@pytest.mark.django_db
def test_image_view_patch_image_only_title(authenticated_api_client):
    user = authenticated_api_client.user
    image = ImageFactory(user=user, file=generate_image_file())

    data = {"title": "New title"}

    response = authenticated_api_client.patch(
        reverse("images:images-detail", args=[image.id]), data=data
    )

    assert response.status_code == 200
    assert response.data["title"] == "New title"
    assert response.data["width"] == image.width
    assert response.data["height"] == image.height
    assert response.data["file"] == f"http://testserver{settings.MEDIA_URL}{image.file}"


@pytest.mark.django_db
def test_image_view_patch_image_only_dimensions(authenticated_api_client):
    user = authenticated_api_client.user
    image = ImageFactory(user=user, file=generate_image_file())

    data = {"width": 100, "height": 100}

    response = authenticated_api_client.patch(
        reverse("images:images-detail", args=[image.id]), data=data
    )

    assert response.status_code == 200
    assert response.data["title"] == image.title
    assert response.data["width"] == 100
    assert response.data["height"] == 100
    assert response.data["file"] == f"http://testserver{settings.MEDIA_URL}{image.file}"


@pytest.mark.django_db
def test_image_view_patch_image_single_dimension(authenticated_api_client):
    user = authenticated_api_client.user
    image = ImageFactory(user=user, file=generate_image_file())

    data = {"width": 100}

    response = authenticated_api_client.patch(
        reverse("images:images-detail", args=[image.id]), data=data
    )

    assert response.status_code == 200
    assert response.data["title"] == image.title
    assert response.data["width"] == 100
    assert response.data["height"] == image.height
    assert response.data["file"] == f"http://testserver{settings.MEDIA_URL}{image.file}"


@pytest.mark.django_db
def test_image_view_patch_image_no_image_owner(authenticated_api_client):
    image = ImageFactory(file=generate_image_file())

    data = {"title": "New title"}

    response = authenticated_api_client.patch(
        reverse("images:images-detail", args=[image.id]), data=data
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_image_view_delete_image(authenticated_api_client):
    user = authenticated_api_client.user
    image = ImageFactory(user=user, file=generate_image_file())

    response = authenticated_api_client.delete(
        reverse("images:images-detail", args=[image.id])
    )

    assert response.status_code == 204
    assert Image.objects.count() == 0


@pytest.mark.django_db
def test_image_view_delete_image_no_image_owner(authenticated_api_client):
    image = ImageFactory(file=generate_image_file())

    response = authenticated_api_client.delete(
        reverse("images:images-detail", args=[image.id])
    )

    assert response.status_code == 404
    assert Image.objects.count() == 1
