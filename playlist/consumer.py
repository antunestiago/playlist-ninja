import json
from channels.generic.websocket import AsyncWebsocketConsumer


class MusicConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the "music_updates" group
        await self.channel_layer.group_add(
            "music_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the "music_updates" group
        await self.channel_layer.group_discard(
            "music_updates",
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        # Broadcast the received message to all clients in the "music_updates" group
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            "music_updates",
            {
                "type": "music_update",
                "message": message
            }
        )

    async def music_update(self, event):
        # Send the event data to the WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
