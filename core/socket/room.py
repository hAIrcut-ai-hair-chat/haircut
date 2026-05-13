import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from core.tasks import chatAI_teste

from core.models import User, Room


logger = logging.getLogger(__name__)


class RoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            self.room_id = self.scope["url_route"]["kwargs"]["room_id"]

            self.room_group_name = f"room_{self.room_id}"

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

            logger.info(
                f"Connected to room {self.room_group_name}"
            )

        except Exception as e:
            logger.error(f"Connection error: {e}")

            await self.close()

    @database_sync_to_async
    def get_or_create_room(self, room_uuid):
        room, _ = Room.objects.get_or_create(
            uuid=room_uuid
        )

        return room

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
                "profile_image": (
                    "Ainda não há uma imagem de perfil"
                )
            }

        except User.DoesNotExist:
            raise ValueError("User not found")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            message = data.get("message")

            if not message:
                return

            logger.info(
                f"Message received: {message}"
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message
                }
            )

        except json.JSONDecodeError:
            logger.error("Invalid JSON")

        except Exception as e:
            logger.error(f"Receive error: {e}")

    async def chat_message(self, event):
        try:
            message = event["message"]

            await self.send(
                text_data=json.dumps({
                    "message": chatAI_teste()
                })
            )

        except Exception as e:
            logger.error(f"Send error: {e}")

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

            logger.info(
                f"Disconnected from room {self.room_group_name}"
            )

        except Exception as e:
            logger.error(f"Disconnect error: {e}")