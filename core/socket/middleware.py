from encodings.idna import ace_prefix
from os import access
from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from httpx import get
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser

from core.models import User

@database_sync_to_async
def get_user(token):
    try:
        access_token = AccessToken(token=token)
        user_uuid = access_token["uuid"]
        return User.objects.get(uuid=user_uuid)
    except Exception:
        return AnonymousUser
    
class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        query_params = parse_qs(query_string)
        token = query_params.get('token')


        scope["user"] = AnonymousUser()

        if token:
            scope["user"] = await get_user(token[0])
        
        return await super().__call__(scope, receive, send)
