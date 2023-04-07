from ninja import NinjaAPI
from .endpoints.author import router as author_router
from .endpoints.album import router as album_router
from .endpoints.song import router as song_router

api = NinjaAPI()
api.add_router("/authors", author_router)
api.add_router("/albums", album_router)
api.add_router("/songs", song_router)
