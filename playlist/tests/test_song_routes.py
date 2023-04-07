import json
from django.urls import reverse
import pytest

from playlist.models import Song, Author, Album


@pytest.fixture
def populate_db():
    # Create 10 authors
    authors = []
    for i in range(1, 11):
        name = f"Author {i}"
        author = Author.objects.create(name=name)
        authors.append(author)

    # Create 10 albums (1 per author)
    albums = []
    for i in range(0, 10):
        title1 = f"Album {i+1}a"
        album1 = Album.objects.create(title=title1, author=authors[i])
        albums.append(album1)

    # Create 30 songs (3 per author, 3 per album)
    songs = []
    for i in range(0, 10):
        title1 = f"Song {i+1}a"
        title2 = f"Song {i+1}b"
        title3 = f"Song {i+1}c"
        song1 = Song.objects.create(title=title1, author=authors[i], album=albums[i], duration=168)
        song2 = Song.objects.create(title=title2, author=authors[i], album=albums[i], duration=170)
        song3 = Song.objects.create(title=title3, author=authors[i], album=albums[i], duration=190)
        songs.append(song1)
        songs.append(song2)
        songs.append(song3)

    yield

    # Teardown: delete all created instances
    for album in albums:
        album.delete()
    for author in authors:
        author.delete()
    for song in songs:
        song.delete()


@pytest.mark.django_db
def test_create_song(client):
    url = reverse("api-1.0.0:create_song")

    author = Author.objects.create(name="John Doe")
    album = Album.objects.create(title="Album One", author=author)

    payload = {
        "title": "Album One",
        "duration": 180,
        "author_id": author.id,
        "album_id": album.id
    }

    response = client.post(url, json.dumps(payload), content_type="application/json")

    response_data = response.json()
    assert response.status_code == 201
    assert response_data["title"] == payload["title"]
    assert response_data["author"]['id'] == author.id
    assert response_data["album"]['id'] == author.id


@pytest.mark.django_db
def test_list_songs(client, populate_db):
    url = reverse("api-1.0.0:list_songs")

    response = client.get(url)

    response_data = response.json()

    assert response.status_code == 200
    assert response_data['count'] == 30


@pytest.mark.django_db
def test_get_song(client):
    author = Author.objects.create(name="John Doe")
    album = Album.objects.create(title="Album One", author=author)
    song = Song.objects.create(title="Song 1", author=author, album=album, duration=125)

    url = reverse("api-1.0.0:get_song", kwargs={"song_id": song.id})

    response = client.get(url)

    response_data = response.json()

    assert response.status_code == 200
    assert response_data["title"] == song.title


@pytest.mark.django_db
def test_get_song_not_found(client):
    url = reverse("api-1.0.0:get_song", kwargs={"song_id": 999})

    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_update_song(client):
    author = Author.objects.create(name="John Doe")
    album = Album.objects.create(title="Album One", author=author)
    song = Song.objects.create(title="Song 1", author=author, album=album, duration=125)

    url = reverse("api-1.0.0:update_song", kwargs={"song_id": song.id})

    payload = {
        "title": "Novo nome de song",
        "duration": "120",
        "author_id": author.id,
        "album_id": album.id
    }

    assert song.title != payload['title']

    response = client.put(url, json.dumps(payload), content_type="application/json")

    response_data = response.json()

    assert response.status_code == 200
    assert response_data["title"] == payload["title"]


@pytest.mark.django_db
def test_update_song_not_found(client):
    url = reverse("api-1.0.0:update_song", kwargs={"song_id": 999})

    payload = {
        "title": "Novo nome de song",
        "duration": "120",
        "author_id": 2,
        "album_id": 1
    }

    response = client.put(url, json.dumps(payload), content_type="application/json")

    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_song(client):
    author = Author.objects.create(name="John Doe")
    album = Album.objects.create(title="Album One", author=author)
    song = Song.objects.create(title="Song 1", author=author, album=album, duration=125)

    url = reverse("api-1.0.0:delete_song", kwargs={"song_id": song.id})

    response = client.delete(url, content_type="application/json")

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_song_not_found(client):
    url = reverse("api-1.0.0:delete_song", kwargs={"song_id": 999})

    response = client.delete(url, content_type="application/json")

    assert response.status_code == 404
