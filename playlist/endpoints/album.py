from django.shortcuts import get_object_or_404
from ninja import Router
from playlist.models import Album, Author
from playlist.schemas import AlbumIn, AlbumOut, AlbumListOut

router = Router(tags=["Albums"])


@router.post("/", response={201: AlbumOut})
def create_album(request, album: AlbumIn):
    album_obj = Album.objects.create(**album.dict())
    return album_obj


@router.get("/albums/", response=AlbumListOut)
def list_albums(request):
    albums = Album.objects.all()
    album_outs = [AlbumOut.from_orm(album) for album in albums]
    return {"items": album_outs, "count": albums.count()}


@router.get("/{album_id}", response=AlbumOut)
def get_album(request, album_id: int):
    album = get_object_or_404(Album, id=album_id)
    return album


@router.put("/{album_id}", response=AlbumOut)
def update_album(request, album_id: int, payload: AlbumIn):
    album = get_object_or_404(Album, id=album_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(album, attr, value)
    album.save()
    return album


@router.delete("/{album_id}")
def delete_album(request, album_id: int):
    album = get_object_or_404(Author, id=album_id)
    album.delete()
    return {"message": f"Album with id {album_id} deleted successfully."}
