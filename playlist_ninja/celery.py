# from asgiref.sync import async_to_sync
from celery import shared_task
# from channels.layers import get_channel_layer
import os
from celery import Celery
from playlist.redis import RedisClient
from playlist.utils.enums import MusicState


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "playlist_ninja.settings")
app = Celery("playlist_ninja")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@shared_task
def song_complete(song_id):
    # Set the state to IDLE in Redis
    redis_client = RedisClient()
    redis_client.set_music_state(str(song_id), MusicState.IDLE.value)

    # Send a WebSocket message to all clients
    # channel_layer = get_channel_layer()
    # async_to_sync(channel_layer.group_send)(
    #     "music_updates",
    #     {
    #         "type": "music_update",
    #         "message": f"Song {song_id} has completed",
    #     },
    # )

