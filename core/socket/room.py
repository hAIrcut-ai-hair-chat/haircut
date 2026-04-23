import logging
from channels.consumer import AsyncConsumer, database_sync_to_async
from regex import P
from rich.pretty import data
from core.models import User, Room


class RoomConsumer(AsyncConsumer):
    async def websocker_connect(self, event):
        logging.info("connected to websocket")
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        logging.info("message received from websocket")
        await self.send({
            "type": "websocket.send",
            "text": event.get("text", "")
        })


    @database_sync_to_async
    def get_or_create_room(self, user_uuid, room_uuid: str | None = None):
        room, _ = Room.objects.get_or_create(user_uuid=user_uuid, uuid=room_uuid)

        return room
        

    async def receive(self, event):
        pass


    @database_sync_to_async
    def get_user(self, uuid):
        if not uuid:
            raise ValueError("UUID is required to fetch user")
        
        try:
            user = User.objects.get(uuid=uuid)
            return {
                "uuid": str(user.uuid),
                "email": user.email,
                "name": user.name,
                "profile_image": "Ainda não há uma imagem de perfil"  # Placeholder, update when profile image is implemented
            }
        except User.DoesNotExist:
            raise ValueError("User with the provided UUID does not exist")
        
         
        
    async def websocket_disconnect(self, event):
        pass
        



    