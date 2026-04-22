import logging
from channels.consumer import AsyncConsumer, database_sync_to_async

from app.settings import DATABASES

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
    def get_db_connnection(self):
        pass

    