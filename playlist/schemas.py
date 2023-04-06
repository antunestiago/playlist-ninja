from typing import List, Optional
from ninja import Schema


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
    name: str
    duration: int
    album_id: int


class SongOut(Schema):
    id: int
    name: str
    duration: int
    album: AlbumOut


class AlbumListOut(Schema):
    items: List[AlbumOut]
    count: int


class SongListOut(Schema):
    items: List[SongOut]
    count: int
