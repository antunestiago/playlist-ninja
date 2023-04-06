from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router
from playlist.models import Author
from playlist.schemas import AuthorIn, AuthorOut

router = Router(tags=["Authors"])


@router.post("/", response={201: AuthorOut})
def create_author(request, payload: AuthorIn):
    author = Author.objects.create(**payload.dict())
    return author


@router.get("/", response=List[AuthorOut])
def list_authors(request):
    authors = Author.objects.all()
    return authors


@router.get("/{author_id}", response=AuthorOut)
def get_author(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    return author


@router.put("/{author_id}", response=AuthorOut)
def update_author(request, author_id: int, payload: AuthorIn):
    author = get_object_or_404(Author, id=author_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(author, attr, value)
    author.save()
    return author


@router.delete("/{author_id}")
def delete_author(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    author.delete()
    return {"message": f"Author with id {author_id} deleted successfully."}
