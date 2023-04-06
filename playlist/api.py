from ninja import Router, NinjaAPI
from .endpoints.author import router as author_router

api = NinjaAPI()
api.add_router("/authors", author_router)
