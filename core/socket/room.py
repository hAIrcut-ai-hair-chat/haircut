import logging
from channels.consumer import AsyncConsumer, database_sync_to_async
from core.models import User, Room
import json


class RoomConsumer(AsyncConsumer):


    async def websocker_connect(self, event):
        logging.info("connected to websocket")
        await self.send({
            "type": "websocket.accept"
        })
        self.accept()

    @database_sync_to_async
    def get_or_create_room(self, user_uuid, room_uuid: str | None = None):
        room, _ = Room.objects.get_or_create(user_uuid=user_uuid, uuid=room_uuid)

        return room


    async def receive(self, event):
        data = json.loads(event['text'])
        message = data.get("message")

        self.send(text_data=json.dumps({
            "message": f"Você disse: {message}"
        }))


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
                "profile_image": "Ainda não há uma imagem de perfil"  
            }
        except User.DoesNotExist:
            raise ValueError("User with the provided UUID does not exist")
        
         
        
    async def websocket_disconnect(self, event):
        pass
        



    