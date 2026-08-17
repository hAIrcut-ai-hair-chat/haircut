import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.exceptions import ValidationError

from core.models import Post
from core.models.room import Room
from core.serializers import PostSerializer

logger = logging.getLogger(__name__)


class FeedRoom(AsyncJsonWebsocketConsumer):

    async def connect(self):
        logging.log(level=1, msg="Ola")
        self.user = self.scope.get("user")

        if self.user is None or self.user.is_anonymous:
            await self.close(code=4001)
            return

        self.room = self.scope["url_route"]["kwargs"].get("room_id")

        if not self.room:
            await self.close(code=4002)
            return

        room_exists = await self.room_exists(self.room)
        if not room_exists:
            await self.close(code=4004)
            return

        try:
            await self.channel_layer.group_add(
                self.room,
                self.channel_name
            )
            await self.accept()
        except Exception:
            logger.exception("Erro ao conectar na sala %s", self.room)
            await self.close(code=4000)

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.room,
                self.channel_name
            )
        except Exception:
            logger.exception("Erro ao desconectar da sala %s", getattr(self, "room", None))

    async def receive_json(self, content, **kwargs):
        text = content.get("text")
        image = content.get("image")

        if not text and not image:
            await self.send_json({
                "error": "É necessário enviar 'text' ou 'image'."
            })
            return

        try:
            post = await self.save_message(self.user, self.room, text, image)
        except ValidationError as e:
            await self.send_json({"error": str(e)})
            return
        except Exception:
            logger.exception("Erro ao salvar mensagem na sala %s", self.room)
            await self.send_json({"error": "Erro interno ao salvar a mensagem."})
            return

        try:
            await self.channel_layer.group_send(
                self.room,
                {
                    "type": "feed.message",
                    "post_uuid": post.uuid
                }
            )
        except Exception:
            logger.exception("Erro ao enviar mensagem para o grupo %s", self.room)
            await self.send_json({"error": "Erro ao propagar a mensagem."})

    async def feed_message(self, event):
        post_uuid = event.get("post_uuid")

        try:
            post = await self.get_post(post_uuid)
        except Post.DoesNotExist:
            logger.warning("Post %s não encontrado", post_uuid)
            return
        except Exception:
            logger.exception("Erro ao buscar post %s", post_uuid)
            return

        try:
            serializer = PostSerializer(post)
            await self.send_json({"post": serializer.data})
        except Exception:
            logger.exception("Erro ao serializar/enviar post %s", post_uuid)

    @database_sync_to_async
    def save_message(self, user, room_id, text, image_key):
        if not room_id:
            raise ValidationError("room_id não informado")

        try:
            post = Post.objects.create(
                user=user,
                room_id=room_id,
                text=text,
                image_key=image_key
            )
        except Exception as e:
            logger.exception("Falha ao criar Post")
            raise ValidationError(f"Não foi possível criar o post: {e}")

        return post

    @database_sync_to_async
    def get_post(self, post_id):
        return Post.objects.get(uuid=post_id)

    @database_sync_to_async
    def room_exists(self, room_id):
        try:
            room, created = Room.objects.get_or_create(uuid=room_id)
            return room
        except (ValueError, TypeError):
            return False