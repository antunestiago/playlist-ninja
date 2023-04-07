from typing import List, Optional
from ninja import Schema

from playlist.utils.enums import MusicState


class AuthorIn(Schema):
    name: str


class AuthorOut(Schema):
    id: int
    name: str


class AlbumIn(Schema):
    title: str
    author_id: int


class AlbumOut(Schema):
    id: int
    title: str
    author: AuthorOut


class SongIn(Schema):
    title: str
    duration: int
    album_id: int
    author_id: int


class SongOut(Schema):
    id: int
    title: str
    duration: int
    album: AlbumOut
    author: AuthorOut


class AlbumListOut(Schema):
    items: List[AlbumOut]
    count: int


class SongListOut(Schema):
    items: List[SongOut]
    count: int


class SongStateUpdate(Schema):
    state: MusicState
