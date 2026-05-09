import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from core.models import User, Room


class RoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        logging.info("connected to websocket")

        await self.accept()

    @database_sync_to_async
    def get_or_create_room(self, user_uuid, room_uuid=None):
        room, _ = Room.objects.get_or_create(
            user_uuid=user_uuid,
            uuid=room_uuid
        )
        return room

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        await self.send(text_data=json.dumps({
            "message": f"Você disse: {message}"
        }))

    @database_sync_to_async
    def get_user(self, uuid):
        if not uuid:
            raise ValueError("UUID is required")

        try:
            user = User.objects.get(uuid=uuid)
            return {
                "uuid": str(user.uuid),
                "email": user.email,
                "name": user.name,
                "profile_image": "Ainda não há uma imagem de perfil"
            }
        except User.DoesNotExist:
            raise ValueError("User not found")

    async def disconnect(self, close_code):
        logging.info("WebSocket disconnected")