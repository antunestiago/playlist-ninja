import json
from django.urls import reverse
import pytest

from playlist.models import Author, Album


@pytest.fixture
def populate_db():
    # Create 24 authors
    authors = []
    for i in range(1, 25):
        name = f"Author {i}"
        author = Author.objects.create(name=name)
        authors.append(author)

    # Create 48 albums (2 per author)
    albums = []
    for i in range(0, 24):
        title1 = f"Album {i+1}a"
        title2 = f"Album {i+1}b"
        album1 = Album.objects.create(title=title1, author=authors[i])
        album2 = Album.objects.create(title=title2, author=authors[i])
        albums.append(album1)
        albums.append(album2)

    yield

    # Teardown: delete all created instances
    for album in albums:
        album.delete()
    for author in authors:
        author.delete()


@pytest.mark.django_db
def test_create_album(client):
    url = reverse("api-1.0.0:create_album")

    author = Author.objects.create(name="Nelson Cavaquinho")


    payload = {
        "title": "Album One",
        "author_id": author.id
    }

    response = client.post(url, json.dumps(payload), content_type="application/json")

    response_data = response.json()
    assert response.status_code == 201
    assert response_data["title"] == payload["title"]
    assert response_data["author"]['id'] == author.id


@pytest.mark.django_db
def test_list_albums(client, populate_db):
    url = reverse("api-1.0.0:list_albums")

    response = client.get(url)

    response_data = response.json()

    assert response.status_code == 200
    assert response_data['count'] == 48


@pytest.mark.django_db
def test_get_album(client):
    author = Author.objects.create(name="John Doe")
    album = Album.objects.create(title="Album One", author=author)

    url = reverse("api-1.0.0:get_album", kwargs={"album_id": album.id})

    response = client.get(url)

    response_data = response.json()

    assert response.status_code == 200
    assert response_data["title"] == album.title


@pytest.mark.django_db
def test_get_album_not_found(client):
    url = reverse("api-1.0.0:get_album", kwargs={"album_id": 999})

    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_update_album(client):
    author = Author.objects.create(name="John Doe")
    album = Album.objects.create(title="Album One", author=author)

    url = reverse("api-1.0.0:update_album", kwargs={"album_id": album.id})

    payload = {
        "title": "Novo nome de album",
        "author_id": author.id
    }

    assert album.title != payload['title']

    response = client.put(url, json.dumps(payload), content_type="application/json")

    response_data = response.json()

    assert response.status_code == 200
    assert response_data["title"] == payload["title"]


@pytest.mark.django_db
def test_update_album_not_found(client):
    url = reverse("api-1.0.0:update_album", kwargs={"album_id": 999})

    payload = {
        "title": "Novo nome de album",
        "author_id": 2
    }

    response = client.put(url, json.dumps(payload), content_type="application/json")

    assert response.status_code == 404

@pytest.mark.django_db
def test_delete_album(client):
    author = Author.objects.create(name="John Doe")
    album = Album.objects.create(title="Album One", author=author)

    url = reverse("api-1.0.0:delete_album", kwargs={"album_id": album.id})

    response = client.delete(url, content_type="application/json")

    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_album_not_found(client):
    url = reverse("api-1.0.0:delete_album", kwargs={"album_id": 999})

    response = client.delete(url, content_type="application/json")

    assert response.status_code == 404
