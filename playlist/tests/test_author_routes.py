import json
from django.urls import reverse
import pytest

from playlist.models import Author


# CREATE AUTHOR TESTS

@pytest.mark.django_db
def test_create_author(client):
    url = reverse("api-1.0.0:create_author")

    payload = {
        "name": "Nelson Cavaquinho",
    }

    response = client.post(url, json.dumps(payload), content_type="application/json")

    response_data = response.json()
    assert response.status_code == 201
    assert response_data["name"] == payload["name"]


@pytest.mark.django_db
def test_list_authors(client):
    url = reverse("api-1.0.0:list_authors")

    Author.objects.create(name="Author 1")
    Author.objects.create(name="Author 2")

    response = client.get(url)

    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 2
    assert response_data[0]["name"] == "Author 1"
    assert response_data[1]["name"] == "Author 2"


# GET AUTHOR TESTS
@pytest.mark.django_db
def test_get_author(client):
    author = Author.objects.create(name="John Doe")
    url = reverse("api-1.0.0:get_author", kwargs={"author_id": author.id})

    response = client.get(url)

    response_data = response.json()

    assert response.status_code == 200
    assert response_data["name"] == "John Doe"

#
# def test_get_author_not_found(client):
#     url = reverse("author-detail", kwargs={"author_id": 999})
#
#     response = client.get(url)
#
#     assert response.status_code == status.HTTP_404_NOT_FOUND
#
#
# # UPDATE AUTHOR TESTS
#
# def test_update_author(client):
#     author = Author.objects.create(name="John Doe", bio="A famous author", birthdate="1980-01-01")
#     url = reverse("author-detail", kwargs={"author_id": author.id})
#
#     payload = {
#         "name": "Jane Doe",
#         "bio": "An even more famous author",
#         "birthdate": "1970-01-01"
#     }
#
#     response = client.put(url, json.dumps(payload), content_type="application/json")
#
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data["name"] == payload["name"]
#     assert response.data["bio"] == payload["bio"]
#     assert response.data["birthdate"] == payload["birthdate"]
#
#
# def test_update_author_not_found(client):
#     url = reverse("author-detail", kwargs={"author_id": 999})
#
#     payload = {
#         "name": "Jane Doe",
#         "bio": "An even more famous author",
#         "birthdate": "1970-01-01"
#     }
#
#     response = client.put(url, json.dumps(payload), content_type="application/json")
#
#     assert response.status_code == status.HTTP_404_NOT_FOUND


