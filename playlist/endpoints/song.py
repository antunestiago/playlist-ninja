from django.shortcuts import get_object_or_404
from ninja import Router
from playlist.models import Song
from playlist.schemas import SongIn, SongOut, SongListOut
from django.db.models import Q

router = Router(tags=["Songs"])


@router.post("/", response={201: SongOut})
def create_song(request, song: SongIn):
    song_obj = Song.objects.create(**song.dict())
    return song_obj


@router.get("/songs/", response=SongListOut)
def list_songs(request, title: str = None, album: str = None, author: str = None):
    query = Q()

    if title:
        query &= Q(title__icontains=title)

    if album:
        query &= Q(album__title__icontains=album)

    if author:
        query &= Q(author__name__icontains=author)

    songs = Song.objects.filter(query)

    songs = songs.prefetch_related('album', 'author')

    song_outs = [SongOut.from_orm(song) for song in songs]
    return {"items": song_outs, "count": songs.count()}


@router.get("/{song_id}", response=SongOut)
def get_song(request, song_id: int):
    song = get_object_or_404(Song, id=song_id)
    return song


@router.put("/{song_id}", response=SongOut)
def update_song(request, song_id: int, payload: SongIn):
    song = get_object_or_404(Song, id=song_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(song, attr, value)
    song.save()
    return song


@router.delete("/{song_id}")
def delete_song(request, song_id: int):
    song = get_object_or_404(Song, id=song_id)
    song.delete()
    return {"message": f"Song with id {song_id} deleted successfully."}
