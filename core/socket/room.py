import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.exceptions import ValidationError

from core.models import Post
from core.models.room import Room
from core.serializers import ListPostSerializer
from core.serializers import PostSerializer

logger = logging.getLogger(__name__)


class FeedRoom(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.user = self.scope.get("user")

        if self.user is None or self.user.is_anonymous:
            await self.close(code=4001)
            return

        self.room = self.scope["url_route"]["kwargs"]["feed_uuid"]

        if not self.room:
            await self.close(code=4002)
            return

        room = await self.room_exists(
            self.room,
            self.user
        )

        if room is None:
            await self.close(code=4004)
            return

        self.room_group_name = f"feed_{self.room}"

        try:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

            logger.info(
                "WebSocket conectado: user=%s room=%s group=%s",
                self.user.id,
                self.room,
                self.room_group_name
            )

            posts = await self.get_posts()

            await self.send_json({
                "posts": posts
            })

        except Exception:
            logger.exception(
                "Erro ao conectar na sala %s",
                self.room
            )

            await self.close(code=4000)

    async def disconnect(self, close_code):
        if not hasattr(self, "room_group_name"):
            return

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        logger.info("WebSocket desconectado: user=%s room=%s code=%s",
            self.user.id,
            self.room,
            close_code
        )

    async def receive_json(self, content, **kwargs):
        print("RECEBEU", content)

        logger.info("Mensagem recebida via WebSocket: %s",content)

        text = content.get("text")
        image = content.get("image")

        if not text and not image:
            await self.send_json({
                "error": "É necessário enviar 'text' ou 'image'."
            })
            return

        try:
            post = await self.save_message(
                self.user,
                self.room,
                text,
                image
            )

        except ValidationError as e:
            logger.warning(
                "Erro de validação: %s",
                e
            )

            await self.send_json({
                "error": str(e)
            })

            return

        except Exception:
            logger.exception(
                "Erro ao salvar post"
            )

            await self.send_json({
                "error": "Erro interno ao salvar a postagem."
            })

            return

        logger.info(
            "Post criado: %s",
            post.uuid
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "feed.message",
                "post_uuid": str(post.uuid)
            }
        )

    async def feed_message(self, event):
        post_uuid = event.get("post_uuid")

        logger.info(
            "Propagando post: %s",
            post_uuid
        )

        try:
            post = await self.get_post(post_uuid)

        except Post.DoesNotExist:
            logger.warning(
                "Post %s não encontrado",
                post_uuid
            )
            return

        except Exception:
            logger.exception(
                "Erro ao buscar post %s",
                post_uuid
            )
            return

        try:
            serializer = PostSerializer(post)

            await self.send_json({
                "post": serializer.data
            })

        except Exception:
            logger.exception("Erro ao serializar post %s", post_uuid)

    @database_sync_to_async
    def save_message(self, user, room_id, text, image_key):
        if not room_id:
            raise ValidationError("room_id não informado")

        try:
            return Post.objects.create(
                author_comment=text,
                image=image_key
                
            )

        except Exception as e:
            logger.exception("Falha ao criar Post")

            raise ValidationError(f"Não foi possível criar o post: {e}")

    @database_sync_to_async
    def get_post(self, post_uuid):
        return Post.objects.get(uuid=post_uuid)

    @database_sync_to_async
    def get_posts(self):
        posts = Post.objects.all()

        serializer = ListPostSerializer(posts, many=True)

        return serializer.data

    @database_sync_to_async
    def room_exists(self, room_id, user):
        try:
            room, created = Room.objects.get_or_create(uuid=room_id, defaults={"user": user})
            return room
        except (ValueError, TypeError):
            return None