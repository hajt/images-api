import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_user_view_authenticated(authenticated_api_client):
    response = authenticated_api_client.get(reverse("users:me"))
    user = authenticated_api_client.user

    expected_response = {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_user_view_unauthenticated(api_client):
    response = api_client.get(reverse("users:me"))

    assert response.status_code == 401
